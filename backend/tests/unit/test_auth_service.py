import pytest
from app.services.auth_service import validate_friend_password


class TestAuthService:
    def test_validate_friend_password_json_format(self, monkeypatch):
        """Test password validation with JSON format."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {
                "friend_passwords": '{"friend1": "password1", "friend2": "password2"}'
            })()
        )
        from app.services.auth_service import settings
        assert validate_friend_password("password1") == "friend1"
        assert validate_friend_password("password2") == "friend2"
        assert validate_friend_password("wrong") is None

    def test_validate_friend_password_comma_separated_format(self, monkeypatch):
        """Test password validation with comma-separated format."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {
                "friend_passwords": "alice:secret1, bob:secret2"
            })()
        )
        from app.services.auth_service import settings
        assert validate_friend_password("secret1") == "alice"
        assert validate_friend_password("secret2") == "bob"
        assert validate_friend_password("wrong") is None

    def test_validate_friend_password_invalid_format(self, monkeypatch):
        """Test password validation with invalid format."""
        monkeypatch.setattr(
            "app.services.auth_service.settings",
            type("Settings", (), {
                "friend_passwords": "invalid_no_colon_or_json"
            })()
        )
        from app.services.auth_service import settings
        assert validate_friend_password("invalid_no_colon_or_json") is None
