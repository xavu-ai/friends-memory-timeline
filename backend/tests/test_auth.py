import pytest
from httpx import AsyncClient


class TestAuth:
    @pytest.mark.asyncio
    async def test_verify_valid_password(self, async_client: AsyncClient):
        """Test POST /api/v1/auth/verify with valid password returns token."""
        response = await async_client.post(
            "/api/v1/auth/verify",
            json={"password": "valid_password"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "expires_in" in data
        assert data["expires_in"] == 3600

    @pytest.mark.asyncio
    async def test_verify_invalid_password(self, async_client: AsyncClient):
        """Test POST /api/v1/auth/verify with invalid password returns 401."""
        response = await async_client.post(
            "/api/v1/auth/verify",
            json={"password": "wrong_password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid password"

    @pytest.mark.asyncio
    async def test_expired_token_returns_401(self, async_client: AsyncClient):
        """Test that an invalid/expired token returns 401."""
        response = await async_client.get(
            "/api/v1/events",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401
