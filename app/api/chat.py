from fastapi import APIRouter, Depends, HTTPException
import httpx
import time
from collections import defaultdict, deque
from openai import APIError, APITimeoutError, AuthenticationError, RateLimitError
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session

from app.agent.orchestration import run_orchestrated_agent
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

        result = run_orchestrated_agent(
            message=request.message,
            db=db,
            session_id=request.session_id,
            confirmed_action=request.action,
        )

        return result
    except HTTPException:
        raise
    except (TimeoutError, requests.exceptions.Timeout, httpx.TimeoutException, APITimeoutError) as e:
        print(f"OpenRouter connection timeout: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=504,
            detail="Koneksi ke OpenRouter timeout. Periksa jaringan server atau coba lagi.",
        ) from e
    except APIError as e:
        print(f"OpenRouter API error: {e}")
        status_code = getattr(e, "status_code", 502)
        error_text = str(e).lower()
        if isinstance(e, AuthenticationError) or "api key" in error_text and "invalid" in error_text:
            status_code = 401
            detail = "OPENROUTER_API_KEY tidak valid. Perbarui API key di file .env lalu restart backend."
        elif isinstance(e, RateLimitError) or status_code in (429, 503):
            status_code = 503
            detail = "Layanan OpenRouter sedang sibuk atau mencapai batas penggunaan. Coba lagi beberapa saat."
        else:
            status_code = status_code if 400 <= status_code < 600 else 502
            detail = "OpenRouter gagal memproses request. Periksa model, endpoint, dan API key."
        raise HTTPException(status_code=status_code, detail=detail) from e
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )