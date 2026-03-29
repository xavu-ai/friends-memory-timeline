from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl


class Settings(BaseSettings):
    database_url: AnyUrl
    friend_passwords: str
    cors_origins: list[str] = ["http://localhost:8100"]
    upload_dir: str = "./uploads"
    max_upload_size: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
