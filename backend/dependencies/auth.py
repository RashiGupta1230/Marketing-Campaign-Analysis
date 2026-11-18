"""
Auth dependency — JWT verification for protected routes.
Usage: `Depends(get_current_user)` on any protected endpoint.
"""
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production-do-not-use-this")
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer(auto_error=False)


class TokenData(BaseModel):
    email: str
    company_id: str
    company_slug: str
    role: str
    name: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TokenData:
    """Validate JWT and return decoded user data. Raise 401 if invalid."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide a Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise ValueError("Missing 'sub' claim in token")
        return TokenData(
            email=email,
            company_id=payload.get("company_id", ""),
            company_slug=payload.get("company_slug", ""),
            role=payload.get("role", "viewer"),
            name=payload.get("name", ""),
        )
    except (JWTError, ValueError, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
