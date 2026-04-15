"""
Production configuration for SmartScreen FastAPI application.
Handles environment-based settings loading.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional
import os
import json

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Configuration
    api_title: str = "SmartScreen API"
    api_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 40
    database_pool_timeout: int = 30
    
    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    cors_origins: str = ""
    
    # Credit System
    resume_parse_credits: int = 5
    jd_parse_credits: int = 3
    match_credits: int = 5
    bulk_analysis_credits: int = 20
    
    # Logging
    log_level: str = "INFO"
    
    # Payment (optional)
    razorpay_key_id: Optional[str] = None
    razorpay_key_secret: Optional[str] = None
    stripe_secret_key: Optional[str] = None
    payment_webhook_secret: Optional[str] = None
    
    # Monitoring (optional)
    sentry_dsn: Optional[str] = None
    app_insights_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        if not self.cors_origins:
            return []
        return [i.strip() for i in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() == "development"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.cors_origins, str):
            try:
                return json.loads(self.cors_origins)
            except:
                return [self.cors_origins]
        return self.cors_origins

# Load settings once at startup
try:
    settings = Settings()
except Exception as e:
    raise RuntimeError(
        f"Failed to load settings from environment: {e}\n"
        f"Make sure .env file exists and contains DATABASE_URL and SECRET_KEY"
    )
