from fastapi import APIRouter, Depends, HTTPException
import httpx
from google.genai.errors import APIError
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session

from app.agent.agent import run_agent
from app.database.dependencies import get_db


router = APIRouter(
    prefix="/chat",
    tags=["AI Agent"]
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message tidak boleh kosong"
            )

        response = run_agent(
            message=request.message,
            db=db,
            session_id=request.session_id
        )

        return {
            "response": response
        }
    except HTTPException:
        raise
    except (TimeoutError, requests.exceptions.Timeout, httpx.TimeoutException) as e:
        print(f"Gemini connection timeout: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=504,
            detail="Koneksi ke Google Gemini timeout. Periksa jaringan Docker atau coba lagi.",
        ) from e
    except APIError as e:
        print(f"Gemini API error: {e}")
        status_code = getattr(e, "code", 500)
        if status_code == 503:
            detail = "Google Gemini sedang sibuk. Coba lagi beberapa saat."
        else:
            detail = "Google Gemini gagal memproses request. Periksa model dan API key."
        raise HTTPException(status_code=status_code, detail=detail) from e
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )