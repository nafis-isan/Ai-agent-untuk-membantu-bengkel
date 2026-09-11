import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.agent.agent import run_agent
from app.database.dependencies import get_db

router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp"])


def _parse_message(payload: dict) -> dict | None:
    try:
        value = payload["entry"][0]["changes"][0]["value"]
        message = value["messages"][0]
        return {"sender": message["from"], "text": message["text"]["body"]}
    except (KeyError, IndexError, TypeError):
        return None


async def _send_message(recipient: str, text: str) -> None:
    token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if not token or not phone_id:
        raise RuntimeError("WhatsApp belum dikonfigurasi")
    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": text[:4096]},
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()


@router.get("")
def verify_webhook(request: Request):
    params = request.query_params
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if verify_token and params.get("hub.verify_token") == verify_token:
        return int(params.get("hub.challenge", "0"))
    raise HTTPException(status_code=403, detail="Token webhook WhatsApp tidak valid")


@router.post("")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    incoming = _parse_message(await request.json())
    if not incoming:
        return {"status": "ignored"}
    result = run_agent(incoming["text"], db, session_id=f"whatsapp:{incoming['sender']}")
    if os.getenv("WHATSAPP_ACCESS_TOKEN") and os.getenv("WHATSAPP_PHONE_NUMBER_ID"):
        await _send_message(incoming["sender"], result["response"])
        return {"status": "sent"}
    return {"status": "processed", "message": "WhatsApp belum dikonfigurasi", "response": result["response"]}
