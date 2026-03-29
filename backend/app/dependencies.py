from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import decode_token

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    """Validate JWT Bearer token and return password_hash."""
    token = credentials.credentials
    password_hash = decode_token(token)
    if password_hash is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return password_hash
