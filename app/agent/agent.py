import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import search_vehicle


load_dotenv()


# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)


# Use a valid Gemini model name
MODEL_NAME = "gemini-3.6-flash"


def run_agent(
    message: str,
    db: Session
) -> str:
    try:
        # Create a simple agent without function calling
        # Just send the message to Gemini and get a response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"""
{SYSTEM_PROMPT}

Pesan pengguna:
{message}
"""
        )

        # If no response text, return error message
        if not response.text:
            return "Maaf, tidak dapat memproses permintaan Anda."

        # For now, just return the text response
        # We can add tool calling support later with a different approach
        return response.text

    except Exception as e:
        print(f"Error in run_agent: {type(e).__name__}: {e}")
        raise