import pytest


class TestAudit:
    @pytest.mark.asyncio
    async def test_get_audit_trail_requires_auth(self, async_client):
        """Test that getting audit trail without auth returns 401."""
        response = await async_client.get("/api/v1/events/00000000-0000-0000-0000-000000000001/audit")
        assert response.status_code == 401
