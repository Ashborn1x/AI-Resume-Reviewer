from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Resume Analyzer"
    app_env: str = "development"
    app_debug: bool = False
    app_secret_key: SecretStr | None = None

    database_url: str = "sqlite:///./app.db"

    upload_dir: Path = Path("uploads")
    max_upload_size_mb: int = Field(default=5, ge=1, le=50)
    allowed_upload_extensions: set[str] = {"pdf", "docx", "txt"}

    ai_model: str = "anthropic.claude-3-5-haiku-20241022-v1:0"
    ai_timeout_seconds: int = Field(default=120, ge=5, le=600)
    aws_region: str = "us-east-1"

    prompt_dir: Path = Path("app/prompts")
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("allowed_upload_extensions", mode="before")
    @classmethod
    def parse_extensions(cls, value: str | set[str] | list[str]) -> set[str]:
        if isinstance(value, str):
            return {item.strip().lower().lstrip(".") for item in value.split(",") if item.strip()}
        return {item.lower().lstrip(".") for item in value}

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
