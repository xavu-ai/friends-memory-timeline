import pytest


class TestHealth:
    @pytest.mark.asyncio
    async def test_health_check(self, async_client):
        """Test GET /healthz returns 200."""
        response = await async_client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
