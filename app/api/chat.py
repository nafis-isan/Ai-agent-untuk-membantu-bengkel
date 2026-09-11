from fastapi import APIRouter, Depends, HTTPException
import httpx
import time
from collections import defaultdict, deque
from google.genai.errors import APIError
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session

from app.agent.agent import run_agent
from app.auth import require_admin
from app.database.dependencies import get_db


router = APIRouter(
    prefix="/chat",
    tags=["AI Agent"]
)

_request_history: dict[str, deque[float]] = defaultdict(deque)
RATE_LIMIT_COUNT = 20
RATE_LIMIT_WINDOW_SECONDS = 60


def _check_rate_limit(session_id: str) -> None:
    now = time.monotonic()
    history = _request_history[session_id]
    while history and now - history[0] > RATE_LIMIT_WINDOW_SECONDS:
        history.popleft()
    if len(history) >= RATE_LIMIT_COUNT:
        raise HTTPException(status_code=429, detail="Terlalu banyak pesan. Coba lagi dalam satu menit.")
    history.append(now)


class ChatRequest(BaseModel):
    message: str = ""
    session_id: str = "default"
    action: dict | None = None


class ChatResponse(BaseModel):
    response: str
    actions: list[dict] = []


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    try:
        if not request.message.strip() and not request.action:
            raise HTTPException(
                status_code=400,
                detail="Message tidak boleh kosong"
            )
        _check_rate_limit(request.session_id)

        result = run_agent(
            message=request.message,
            db=db,
            session_id=request.session_id,
            confirmed_action=request.action,
        )

        return result
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
        error_text = str(e).lower()
        if "api_key_invalid" in error_text or "api key not valid" in error_text:
            status_code = 401
            detail = "GEMINI_API_KEY tidak valid. Perbarui API key di file .env lalu restart backend."
        elif status_code == 503:
            detail = "Google Gemini sedang sibuk. Coba lagi beberapa saat."
        else:
            detail = "Google Gemini gagal memproses request. Periksa model dan API key."
        raise HTTPException(status_code=status_code, detail=detail) from e
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )