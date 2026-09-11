import base64
import hashlib
import hmac
import os
import secrets
import time
import json

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


load_dotenv()

bearer_scheme = HTTPBearer(auto_error=False)
TOKEN_TTL_SECONDS = int(os.getenv("ADMIN_TOKEN_TTL_SECONDS", "28800"))


def _secret() -> bytes:
    value = os.getenv("ADMIN_TOKEN_SECRET")
    if not value:
        raise RuntimeError("ADMIN_TOKEN_SECRET environment variable is required")
    return value.encode("utf-8")


def _password_digest(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)


def verify_admin_credentials(username: str, password: str) -> bool:
    configured_username = os.getenv("ADMIN_USERNAME", "admin")
    configured_password = os.getenv("ADMIN_PASSWORD")
    if not configured_password:
        return False
    return secrets.compare_digest(username, configured_username) and secrets.compare_digest(
        _password_digest(password, b"bengkel-admin-salt"),
        _password_digest(configured_password, b"bengkel-admin-salt"),
    )


def create_access_token(username: str) -> str:
    expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    payload = f"{username}:{expires_at}".encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    signature = hmac.new(_secret(), encoded_payload.encode("ascii"), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"{encoded_payload}.{encoded_signature}"


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autentikasi admin diperlukan")
    try:
        encoded_payload, encoded_signature = credentials.credentials.split(".", 1)
        expected_signature = hmac.new(
            _secret(), encoded_payload.encode("ascii"), hashlib.sha256
        ).digest()
        supplied_signature = base64.urlsafe_b64decode(encoded_signature + "===")
        if not hmac.compare_digest(supplied_signature, expected_signature):
            raise ValueError
        payload = base64.urlsafe_b64decode(encoded_payload + "===").decode("utf-8")
        username, expires_at = payload.rsplit(":", 1)
        if int(expires_at) <= int(time.time()) or not username:
            raise ValueError
        return username
    except (ValueError, TypeError, UnicodeDecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token admin tidak valid")


def sign_action(action: dict, session_id: str) -> str:
    payload = json.dumps(
        {"action": action, "session_id": session_id, "expires_at": int(time.time()) + 600},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    signature = hmac.new(_secret(), encoded_payload.encode("ascii"), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"{encoded_payload}.{encoded_signature}"


def verify_action(token: str, action: dict, session_id: str) -> bool:
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        expected = hmac.new(_secret(), encoded_payload.encode("ascii"), hashlib.sha256).digest()
        supplied = base64.urlsafe_b64decode(encoded_signature + "===")
        payload = json.loads(base64.urlsafe_b64decode(encoded_payload + "===").decode("utf-8"))
        return (
            hmac.compare_digest(supplied, expected)
            and payload["session_id"] == session_id
            and payload["expires_at"] > int(time.time())
            and hmac.compare_digest(
                json.dumps(payload["action"], sort_keys=True, separators=(",", ":")),
                json.dumps(action, sort_keys=True, separators=(",", ":")),
            )
        )
    except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return False