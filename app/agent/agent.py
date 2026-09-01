import os
import json

from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import (
    SEARCH_VEHICLE_TOOL,
    search_vehicle
)


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

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=f"""
{SYSTEM_PROMPT}

Pesan pengguna:
{message}
""",
        tools=[
            SEARCH_VEHICLE_TOOL
        ]
    )

    function_call = None

    for step in interaction.steps:

        if step.type == "function_call":
            function_call = step
            break

    if function_call is None:
        return interaction.output_text

    if function_call.name == "search_vehicle":

        result = search_vehicle(
            plate_number=function_call.arguments["plate_number"],
            db=db
        )

        final_interaction = client.interactions.create(
            model=MODEL_NAME,
            previous_interaction_id=interaction.id,
            input=[
                {
                    "type": "function_result",
                    "name": function_call.name,
                    "call_id": function_call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result)
                        }
                    ]
                }
            ],
            tools=[
                SEARCH_VEHICLE_TOOL
            ]
        )

        return final_interaction.output_text

    return "Maaf, tool yang diminta belum tersedia."