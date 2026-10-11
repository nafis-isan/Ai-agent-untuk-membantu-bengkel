import json
import os
import hashlib
import logging
import time
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from openai import APIError, OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.agent.memory import conversation_memory
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import TOOL_DECLARATIONS, TOOL_FUNCTIONS, create_service, update_service_status, validate_tool_arguments
from app.auth import sign_action, verify_action
from app.database.models import AgentUsage, UsedAction


load_dotenv()
logger = logging.getLogger("bengkel.agent")
MAX_MESSAGE_LENGTH = 4000
INJECTION_PATTERNS = ("ignore previous instructions", "abaikan semua aturan", "system prompt", "jailbreak")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    timeout=30.0,
    max_retries=0,
)
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free")


def _tool_config() -> list[dict]:
    def normalize_schema(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: normalize_schema(item.lower() if key == "type" and isinstance(item, str) else item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [normalize_schema(item) for item in value]
        return value

    return [
        {
            "type": "function",
            "function": {
                "name": declaration["name"],
                "description": declaration["description"],
                "parameters": normalize_schema(declaration["parameters"]),
            },
        }
        for declaration in TOOL_DECLARATIONS
    ]


def _generate_content(prompt: str, tools: bool, session_id: str) -> Any:
    for retry in range(2):
        started = time.perf_counter()
        try:
            request = {
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
            if tools:
                request["tools"] = _tool_config()
            response = client.chat.completions.create(**request)
            logger.info("llm_request session=%s retry=%s duration_ms=%s", session_id, retry, round((time.perf_counter() - started) * 1000, 2))
            return response
        except (TimeoutError, APIError):
            logger.warning("llm_retry session=%s retry=%s duration_ms=%s", session_id, retry, round((time.perf_counter() - started) * 1000, 2), exc_info=True)
            if retry == 1:
                raise
            time.sleep(0.25 * (retry + 1))
    raise RuntimeError("LLM request gagal")


def _call_tools(response: Any, db: Session, session_id: str) -> tuple[list[dict], list[dict]]:
    results = []
    actions = []
    message = response.choices[0].message
    for tool_call in getattr(message, "tool_calls", None) or []:
        name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments or "{}")
        except json.JSONDecodeError:
            results.append({"tool": name, "error": "Parameter tool tidak valid."})
            logger.warning("tool_arguments_invalid session=%s tool=%s", session_id, name)
            continue
        if not isinstance(arguments, dict):
            results.append({"tool": name, "error": "Parameter tool tidak valid."})
            logger.warning("tool_arguments_invalid session=%s tool=%s", session_id, name)
            continue
        function = TOOL_FUNCTIONS.get(name)
        if function is None:
            results.append({"tool": name, "error": "Tool tidak tersedia."})
            continue
        valid_arguments, validation_error = validate_tool_arguments(name, arguments)
        if validation_error:
            results.append({"tool": name, "error": validation_error})
            logger.warning("tool_validation_failed session=%s tool=%s error=%s", session_id, name, validation_error)
            continue
        started = time.perf_counter()
        try:
            result = function(db=db, **valid_arguments)
        except Exception as error:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.exception("tool_failed session=%s tool=%s duration_ms=%s", session_id, name, duration_ms)
            results.append({"tool": name, "error": "Tool gagal diproses."})
            continue
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info("tool_trajectory session=%s tool=%s arguments=%s duration_ms=%s result_keys=%s", session_id, name, valid_arguments, duration_ms, list(result.keys()))
        results.append({"tool": name, "result": result})
        if result.get("action"):
            action = result["action"]
            action["confirmation_token"] = sign_action(action, session_id)
            actions.append(action)
    return results, actions


def _execute_confirmed_action(action: dict, db: Session, session_id: str) -> str:
    confirmation_token = action.pop("confirmation_token", "")
    if not verify_action(confirmation_token, action, session_id):
        raise ValueError("Konfirmasi tindakan tidak valid atau sudah kedaluwarsa.")
    token_hash = hashlib.sha256(confirmation_token.encode("utf-8")).hexdigest()
    if db.query(UsedAction).filter(UsedAction.token_hash == token_hash).first():
        raise ValueError("Konfirmasi tindakan sudah pernah digunakan.")
    db.add(UsedAction(token_hash=token_hash))
    db.flush()
    if action.get("type") == "update_service_status":
        result = update_service_status(action.get("payload", {}), db)
        return f"Status servis #{result['id']} berhasil diubah menjadi {result['status']}."
    if action.get("type") != "create_service":
        raise ValueError("Action tidak dikenali.")
    result = create_service(action.get("payload", {}), db)
    return f"Servis #{result['id']} berhasil dibuat dan masuk ke antrean dengan status {result['status']}."


def run_agent(
    message: str,
    db: Session,
    session_id: str = "default",
    confirmed_action: dict | None = None,
    system_prompt: str | None = None,
) -> dict[str, Any]:
    normalized_message = message.strip()
    if not normalized_message:
        raise ValueError("Pesan tidak boleh kosong.")
    if len(normalized_message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Pesan terlalu panjang. Maksimal {MAX_MESSAGE_LENGTH} karakter.")
    if any(pattern in normalized_message.lower() for pattern in INJECTION_PATTERNS):
        response_text = "Saya tetap mengikuti aturan operasional BengkelAI. Silakan tanyakan tentang pelanggan, kendaraan, servis, atau suku cadang."
        conversation_memory.add(db, session_id, "user", normalized_message)
        conversation_memory.add(db, session_id, "assistant", response_text)
        return {"response": response_text, "actions": [], "metrics": {"tool_calls": 0, "attempts": 0}}
    message = normalized_message
    if confirmed_action:
        response_text = _execute_confirmed_action(confirmed_action, db, session_id)
        conversation_memory.add(db, session_id, "user", "Konfirmasi tindakan servis")
        conversation_memory.add(db, session_id, "assistant", response_text)
        return {"response": response_text, "actions": [], "metrics": {"tool_calls": 0, "attempts": 0}}

    history = conversation_memory.get(db, session_id)
    history_text = "\n".join(
        f"{item['role'].capitalize()}: {item['content']}" for item in history
    )
    prompt = system_prompt or SYSTEM_PROMPT
    if history_text:
        prompt += f"\n\nRiwayat percakapan:\n{history_text}"
    prompt += f"\n\nPesan pengguna:\n{message}"

    actions: list[dict] = []
    response_text = ""
    tool_call_count = 0
    attempt_count = 0
    for attempt in range(2):
        attempt_count += 1
        daily_budget = float(os.getenv("OPENROUTER_DAILY_BUDGET_USD", "0"))
        if daily_budget:
            start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            spent = db.query(func.coalesce(func.sum(AgentUsage.estimated_cost), 0)).filter(AgentUsage.created_at >= start_of_day).scalar()
            if float(spent or 0) >= daily_budget:
                raise RuntimeError("Batas biaya AI harian telah tercapai.")
        response = _generate_content(
            prompt,
            tools=attempt == 0,
            session_id=session_id,
        )
        usage = getattr(response, "usage", None)
        input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        estimated_cost = (
            input_tokens * float(os.getenv("OPENROUTER_INPUT_COST_PER_1M", "0"))
            + output_tokens * float(os.getenv("OPENROUTER_OUTPUT_COST_PER_1M", "0"))
        ) / 1_000_000
        db.add(AgentUsage(session_id=session_id, model=MODEL_NAME, input_tokens=input_tokens, output_tokens=output_tokens, estimated_cost=estimated_cost))
        db.commit()
        logger.info("agent_request session=%s model=%s input_tokens=%s output_tokens=%s estimated_cost=%.6f", session_id, MODEL_NAME, input_tokens, output_tokens, estimated_cost)
        tool_results, new_actions = _call_tools(response, db, session_id)
        tool_call_count += len(getattr(response.choices[0].message, "tool_calls", None) or [])
        actions.extend(new_actions)
        if not tool_results:
            response_text = (response.choices[0].message.content or "").strip() or "Maaf, tidak dapat memproses permintaan Anda."
            break
        if actions:
            response_text = "Saya sudah menyiapkan tindakan berikut. Mohon konfirmasi sebelum menyimpan data."
            break
        prompt += f"\n\nHasil tool database:\n{json.dumps(tool_results, ensure_ascii=False, default=str)}\nGunakan hasil ini untuk menjawab pengguna secara ringkas."

    if not response_text:
        response_text = "Data berhasil diproses, tetapi AI tidak menghasilkan ringkasan teks. Silakan coba pertanyaan yang lebih spesifik."

    conversation_memory.add(db, session_id, "user", message)
    conversation_memory.add(db, session_id, "assistant", response_text)
    return {
        "response": response_text,
        "actions": actions,
        "metrics": {"tool_calls": tool_call_count, "attempts": attempt_count},
    }
