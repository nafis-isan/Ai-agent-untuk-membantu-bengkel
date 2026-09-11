import json
import os
import hashlib
import logging
import time
from datetime import datetime, timedelta
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from google.genai import types
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

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000),
) if api_key else None
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def _tool_config() -> types.GenerateContentConfig:
    declarations = [
        types.FunctionDeclaration(
            name=declaration["name"],
            description=declaration["description"],
            parameters=declaration["parameters"],
        )
        for declaration in TOOL_DECLARATIONS
    ]
    return types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=declarations)],
        temperature=0.2,
    )


def _text_config() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(temperature=0.2)


def _generate_content(prompt: str, config: types.GenerateContentConfig, session_id: str) -> Any:
    for retry in range(2):
        started = time.perf_counter()
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=config)
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
    for function_call in getattr(response, "function_calls", None) or []:
        name = getattr(function_call, "name", "")
        arguments = dict(getattr(function_call, "args", {}) or {})
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
        return {"response": response_text, "actions": []}
    message = normalized_message
    if confirmed_action:
        response_text = _execute_confirmed_action(confirmed_action, db, session_id)
        conversation_memory.add(db, session_id, "user", "Konfirmasi tindakan servis")
        conversation_memory.add(db, session_id, "assistant", response_text)
        return {"response": response_text, "actions": []}

    history = conversation_memory.get(db, session_id)
    history_text = "\n".join(
        f"{item['role'].capitalize()}: {item['content']}" for item in history
    )
    prompt = SYSTEM_PROMPT
    if history_text:
        prompt += f"\n\nRiwayat percakapan:\n{history_text}"
    prompt += f"\n\nPesan pengguna:\n{message}"

    actions: list[dict] = []
    response_text = ""
    for attempt in range(2):
        if client is None:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set")
        daily_budget = float(os.getenv("GEMINI_DAILY_BUDGET_USD", "0"))
        if daily_budget:
            start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            spent = db.query(func.coalesce(func.sum(AgentUsage.estimated_cost), 0)).filter(AgentUsage.created_at >= start_of_day).scalar()
            if float(spent or 0) >= daily_budget:
                raise RuntimeError("Batas biaya AI harian telah tercapai.")
        response = _generate_content(
            prompt,
            _tool_config() if attempt == 0 else _text_config(),
            session_id,
        )
        usage = getattr(response, "usage_metadata", None)
        input_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
        output_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
        estimated_cost = (
            input_tokens * float(os.getenv("GEMINI_INPUT_COST_PER_1M", "0"))
            + output_tokens * float(os.getenv("GEMINI_OUTPUT_COST_PER_1M", "0"))
        ) / 1_000_000
        db.add(AgentUsage(session_id=session_id, model=MODEL_NAME, input_tokens=input_tokens, output_tokens=output_tokens, estimated_cost=estimated_cost))
        db.commit()
        logger.info("agent_request session=%s model=%s input_tokens=%s output_tokens=%s estimated_cost=%.6f", session_id, MODEL_NAME, input_tokens, output_tokens, estimated_cost)
        tool_results, new_actions = _call_tools(response, db, session_id)
        actions.extend(new_actions)
        if not tool_results:
            response_text = (response.text or "").strip() or "Maaf, tidak dapat memproses permintaan Anda."
            break
        if actions:
            response_text = "Saya sudah menyiapkan tindakan berikut. Mohon konfirmasi sebelum menyimpan data."
            break
        prompt += f"\n\nHasil tool database:\n{json.dumps(tool_results, ensure_ascii=False, default=str)}\nGunakan hasil ini untuk menjawab pengguna secara ringkas."

    if not response_text:
        response_text = "Data berhasil diproses, tetapi AI tidak menghasilkan ringkasan teks. Silakan coba pertanyaan yang lebih spesifik."

    conversation_memory.add(db, session_id, "user", message)
    conversation_memory.add(db, session_id, "assistant", response_text)
    return {"response": response_text, "actions": actions}
