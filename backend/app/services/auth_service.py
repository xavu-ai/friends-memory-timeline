import hashlib
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings


def _hash_password(password: str) -> str:
    """Create a SHA256 hash of the password for audit logging."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str) -> bool:
    """Check if password is in the allowed list."""
    return password in settings.password_list


def create_access_token(password: str) -> tuple[str, int]:
    """Create a JWT access token. Returns (token, expires_in_seconds)."""
    expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    password_hash = _hash_password(password)

    payload = {
        "sub": password_hash,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return token, int(expires_delta.total_seconds())


def decode_token(token: str) -> str | None:
    """Decode JWT and return password_hash (sub) if valid, else None."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "access":
            return None
        return payload.get("sub")
    except Exception:
        return None
