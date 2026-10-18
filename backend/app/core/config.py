from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = Field(default="development")
    DATABASE_URL: str = Field(default="sqlite:///./ventureforge.db")
    JWT_SECRET: str = Field(default="change-me-in-real-env")
    JWT_EXPIRE_MINUTES: int = Field(default=1440)
    CORS_ORIGINS: str = Field(default="http://localhost:3000")
    ANTHROPIC_API_KEY: str = Field(default="")
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="")
    GEMINI_RERANK: bool = Field(default=False)
    GEMINI_TIMEOUT_SECONDS: int = Field(default=8)

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def gemini_api_key(self) -> str:
        return self.GEMINI_API_KEY

    @property
    def gemini_model(self) -> str:
        return self.GEMINI_MODEL

    @property
    def gemini_rerank(self) -> bool:
        return self.GEMINI_RERANK

    @property
    def gemini_timeout_seconds(self) -> int:
        return self.GEMINI_TIMEOUT_SECONDS

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "production"

settings = Settings()
