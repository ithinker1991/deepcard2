"""
Application configuration settings.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "DeepCard API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str

    # Database
    DATABASE_URL: str = "sqlite:///./deepcard.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 1000

    # DeepSeek Settings
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    # SiliconFlow Settings
    SILICONFLOW_API_KEY: str = ""
    SILICONFLOW_MODEL: str = "deepseek-ai/DeepSeek-V3"
    SILICONFLOW_BASE_URL: str = "https://api.siliconflow.cn/v1"

    # LLM Default Settings
    DEFAULT_LLM_PROVIDER: str = "openai"
    LLM_TIMEOUT: int = 30
    LLM_MAX_RETRIES: int = 3

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Content Processing
    MAX_CONTENT_LENGTH: int = 100_000
    DEFAULT_CARD_DIFFICULTY: int = 1
    MAX_CARDS_PER_GENERATION: int = 20

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.DEBUG

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.DEBUG

    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL."""
        if self.DATABASE_URL.startswith("sqlite+aiosqlite"):
            return self.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
        elif self.DATABASE_URL.startswith("postgresql+asyncpg"):
            return self.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
        return self.DATABASE_URL


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()