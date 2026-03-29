from fastapi import APIRouter, HTTPException
from app.schemas.auth import VerifyRequest, VerifyResponse
from app.services.auth_service import verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/verify", response_model=VerifyResponse)
async def verify(request: VerifyRequest) -> VerifyResponse:
    """Verify password and return JWT token."""
    if not verify_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token, expires_in = create_access_token(request.password)
    return VerifyResponse(token=token, expires_in=expires_in)
