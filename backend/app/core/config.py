"""Application runtime settings and environment variable configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads configuration from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Signal Clone API"
    cors_origins: str = "http://localhost:3000"
    database_url: str = "sqlite:///./signal.db"
    media_dir: str = "./media"
    mock_otp: str = "123456"
    demo_mode: bool = True
    seed_on_startup: bool = True
    session_ttl_days: int = 30

    @property
    def cors_origin_list(self) -> list[str]:
        """Parses comma-separated CORS origin strings into a sanitized list of origins."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Returns a cached singleton Settings instance."""
    return Settings()

