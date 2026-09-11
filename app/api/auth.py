from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.auth import create_access_token, verify_admin_credentials


router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    if not verify_admin_credentials(request.username, request.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    return {"access_token": create_access_token(request.username)}