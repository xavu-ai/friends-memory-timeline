import pytest
from app.services.auth_service import verify_password, create_access_token, decode_token


class TestAuthService:
    def test_verify_password_valid(self, monkeypatch):
        """Test verify_password returns True for valid password."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {"password_list": ["pwd1", "pwd2"]})(),
        )
        from app.services.auth_service import settings
        assert verify_password("pwd1") is True
        assert verify_password("pwd2") is True

    def test_verify_password_invalid(self, monkeypatch):
        """Test verify_password returns False for invalid password."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {"password_list": ["pwd1"]})(),
        )
        assert verify_password("wrong") is False

    def test_create_and_decode_token(self, monkeypatch):
        """Test JWT token creation and decoding."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {
                "JWT_SECRET": "test-secret-key-for-testing-only-32chars",
                "JWT_ALGORITHM": "HS256",
                "JWT_EXPIRE_MINUTES": 60,
                "password_list": ["pwd1"],
            })(),
        )
        token, expires_in = create_access_token("pwd1")
        assert expires_in == 3600
        password_hash = decode_token(token)
        assert password_hash is not None

    def test_decode_invalid_token(self, monkeypatch):
        """Test decoding invalid token returns None."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {
                "JWT_SECRET": "test-secret-key-for-testing-only-32chars",
                "JWT_ALGORITHM": "HS256",
            })(),
        )
        assert decode_token("invalid.token.here") is None
