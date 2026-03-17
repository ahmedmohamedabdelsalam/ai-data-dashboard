"""
Application configuration.
Loads settings from environment variables with sensible defaults.
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment."""

    # API
    APP_NAME: str = "AI Data Analysis Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # File upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    ALLOWED_EXTENSIONS: set = {".csv", ".xlsx", ".xls"}

    # LLM (OpenAI or Gemini)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openrouter")  # openai | gemini | openrouter
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "mistralai/mixtral-8x7b-instruct")

    # Analysis defaults
    KMEANS_N_CLUSTERS: int = int(os.getenv("KMEANS_N_CLUSTERS", "5"))
    ISOLATION_FOREST_CONTAMINATION: float = float(
        os.getenv("ISOLATION_FOREST_CONTAMINATION", "0.1")
    )

    def validate(self, logger):
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY is not set. AI insights will be disabled.")
        elif self.LLM_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. AI insights will be disabled.")
        elif self.LLM_PROVIDER == "openrouter" and not self.OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY is not set. AI insights will be disabled.")

settings = Settings()
