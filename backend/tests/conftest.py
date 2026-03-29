import os

# Set test environment variables BEFORE importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("FRIEND_PASSWORDS", '{"test_friend": "test_password"}')
os.environ.setdefault("CORS_ORIGINS", '["http://localhost:8100"]')
os.environ.setdefault("UPLOAD_DIR", "./uploads")
os.environ.setdefault("MAX_UPLOAD_SIZE", "10485760")

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.db.session import get_db
from app.models.base import Base

# Use SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    """Create tables before each test and drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    """Create an async test client with overridden DB session."""
    # Override the get_db dependency to use test DB
    async def override_get_db():
        async with test_async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers():
    """Return auth headers for test friend."""
    return {"Authorization": "Bearer test_password"}


@pytest.fixture
async def db_session():
    """Return a test database session (for service-level tests)."""
    async with test_async_session() as session:
        yield session
