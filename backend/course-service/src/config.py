import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):  # type: ignore
    # Application Settings
    APP_NAME: str = "Course Service"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./course_service.db")

    # Redis Settings (for events and caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # External Services
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8001")
    ENROLLMENT_SERVICE_URL: str = os.getenv(
        "ENROLLMENT_SERVICE_URL", "http://localhost:8002"
    )

    # Feature Flags
    ENABLE_EVENTS: bool = os.getenv("ENABLE_EVENTS", "True").lower() == "true"

    class Config:
        env_file = ".env"


# Create settings instance
settings = Settings()
