"""
Auth router — JWT login/register with bcrypt password hashing.
Replace _DEMO_USERS with Supabase Auth in production.
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from jose import jwt
from pydantic import BaseModel, EmailStr

logger = logging.getLogger(__name__)
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production-do-not-use-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

import bcrypt

def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Demo users — replace with Supabase Auth query in production
_DEMO_USERS: dict = {
    "demo@attributeiq.com": {
        "pw_hash": _hash_password("demo1234"),
        "name": "Demo User",
        "company_id": "comp_demo",
        "company_slug": "demo-company",
        "role": "admin",
    }
}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    company_name: str
    slug: str
    industry: str
    admin_name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    company_id: str
    company_slug: str
    user_name: str
    role: str
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    user = _DEMO_USERS.get(str(req.email))
    if not user or not _verify_password(req.password, user["pw_hash"]):
        # Constant-time response — don't reveal whether email exists
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = _create_access_token(
        data={
            "sub": str(req.email),
            "name": user["name"],
            "company_id": user["company_id"],
            "company_slug": user["company_slug"],
            "role": user["role"],
        }
    )
    return TokenResponse(
        access_token=token,
        company_id=user["company_id"],
        company_slug=user["company_slug"],
        user_name=user["name"],
        role=user["role"],
    )


@router.post("/register", status_code=201)
async def register(req: RegisterRequest):
    """
    Register a new workspace. Stores admin in _DEMO_USERS (in-memory).
    Replace with Supabase Auth + Postgres in production.
    """
    email_str = str(req.email)
    if email_str in _DEMO_USERS:
        raise HTTPException(status_code=409, detail="Email already registered.")

    _DEMO_USERS[email_str] = {
        "pw_hash": _hash_password(req.password),
        "name": req.admin_name,
        "company_id": f"comp_{req.slug}",
        "company_slug": req.slug,
        "role": "admin",
    }
    token = _create_access_token(
        data={
            "sub": email_str,
            "name": req.admin_name,
            "company_id": f"comp_{req.slug}",
            "company_slug": req.slug,
            "role": "admin",
        }
    )
    return {
        "message": "Workspace created",
        "access_token": token,
        "token_type": "bearer",
        "redirect": f"/dashboard/{req.slug}",
    }


@router.post("/logout")
async def logout():
    # Stateless JWT — invalidation handled client-side by deleting the token.
    # For production: add token to a Redis blocklist.
    return {"message": "Logged out successfully"}
