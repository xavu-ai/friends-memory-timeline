from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8100"]
    PASSWORDS: str = "[]"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def password_list(self) -> list[str]:
        import json
        try:
            return json.loads(self.PASSWORDS)
        except json.JSONDecodeError:
            return []


settings = Settings()
