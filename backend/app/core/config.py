import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Dodger Report API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./dodgers.db"
    
    # ESPN API Configuration
    ESPN_BASE_URL: str = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb"
    DODGERS_TEAM_ID: str = "19"
    
    # Weather API Configuration
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_BASE_URL: str = "http://api.weatherapi.com/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Environment Configuration
    ENVIRONMENT: str = "development"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Environment-specific overrides
if os.getenv("ENVIRONMENT") == "development":
    settings.DEBUG = True
    settings.DATABASE_URL = "sqlite:///./dodgers.db"
elif os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
    # Production database URL would be set via environment variable
    settings.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dodgers.db")

# Validate required settings
def validate_settings():
    """
    Validate that all required settings are properly configured.
    """
    if not settings.WEATHER_API_KEY:
        print("⚠️  Warning: WEATHER_API_KEY not set. Weather functionality will be disabled.")
        print("   Get a free API key from: https://www.weatherapi.com/")
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == "your-secret-key-here":
        print("⚠️  Warning: SECRET_KEY not set. Using default value.")
        print("   Set SECRET_KEY environment variable in production.")
    
    print(f"✅ Configuration loaded: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"   Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   Database: {settings.DATABASE_URL}")
    print(f"   Weather API: {'Enabled' if settings.WEATHER_API_KEY else 'Disabled'}")

# Run validation when module is imported
if __name__ != "__main__":
    validate_settings()
