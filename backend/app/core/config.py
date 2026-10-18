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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "production"

settings = Settings()
