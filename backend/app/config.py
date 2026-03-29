from pydantic_settings import BaseSettings, SettingsConfigDict


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
            return list(json.loads(self.PASSWORDS))
        except json.JSONDecodeError:
            return []


settings = Settings()  # type: ignore[call-arg]
