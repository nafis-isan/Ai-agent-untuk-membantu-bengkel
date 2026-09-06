import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.agent.memory import conversation_memory
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import search_vehicle


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000),
)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def run_agent(
    message: str,
    db: Session,
    session_id: str = "default"
) -> str:
    try:
        history = conversation_memory.get(session_id)
        history_text = "\n".join(
            f"{item['role'].capitalize()}: {item['content']}"
            for item in history
        )
        prompt = SYSTEM_PROMPT
        if history_text:
            prompt += f"\n\nRiwayat percakapan:\n{history_text}"
        prompt += f"\n\nPesan pengguna:\n{message}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        response_text = response.text
        if not response_text:
            return "Maaf, tidak dapat memproses permintaan Anda."

        conversation_memory.add(session_id, "user", message)
        conversation_memory.add(session_id, "assistant", response_text)
        return response_text

    except Exception as e:
        print(f"Error in run_agent: {type(e).__name__}: {e}")
        raise