from typing import Optional
from fastapi import HTTPException, Header
from app.services.auth_service import validate_friend_password


async def get_current_friend(authorization: Optional[str] = Header(None)) -> str:
    """Validate Authorization header and return friend_id."""
    if authorization is None:
        raise HTTPException(401, detail={"detail": "Invalid password"})
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, detail={"detail": "Invalid authentication credentials"})
    token = authorization[7:]
    friend_id = validate_friend_password(token)
    if not friend_id:
        raise HTTPException(401, detail={"detail": "Invalid password"})
    return friend_id
