import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.agent.memory import conversation_memory
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import TOOL_DECLARATIONS, TOOL_FUNCTIONS, create_service


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000),
)
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


def _call_tools(response: Any, db: Session) -> tuple[list[dict], list[dict]]:
    results = []
    actions = []
    for function_call in getattr(response, "function_calls", None) or []:
        name = getattr(function_call, "name", "")
        arguments = dict(getattr(function_call, "args", {}) or {})
        function = TOOL_FUNCTIONS.get(name)
        if function is None:
            results.append({"tool": name, "error": "Tool tidak tersedia."})
            continue
        result = function(db=db, **arguments)
        results.append({"tool": name, "result": result})
        if result.get("action"):
            actions.append(result["action"])
    return results, actions


def _execute_confirmed_action(action: dict, db: Session) -> str:
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
    if confirmed_action:
        response_text = _execute_confirmed_action(confirmed_action, db)
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
    for _ in range(2):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=_tool_config(),
        )
        tool_results, new_actions = _call_tools(response, db)
        actions.extend(new_actions)
        if not tool_results:
            response_text = response.text or "Maaf, tidak dapat memproses permintaan Anda."
            break
        if actions:
            response_text = "Saya sudah menyiapkan tindakan berikut. Mohon konfirmasi sebelum menyimpan data."
            break
        prompt += f"\n\nHasil tool database:\n{json.dumps(tool_results, ensure_ascii=False, default=str)}\nGunakan hasil ini untuk menjawab pengguna secara ringkas."

    conversation_memory.add(db, session_id, "user", message)
    conversation_memory.add(db, session_id, "assistant", response_text)
    return {"response": response_text, "actions": actions}
