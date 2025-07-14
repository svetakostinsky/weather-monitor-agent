import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the Weather Monitor Agent."""
    
    # OpenAI Configuration
    openai_api_key: str
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Weather API Configuration
    openweather_api_key: str
    weather_city: str
    weather_country_code: str = "US"
    
    # Email Configuration
    email_sender: str
    email_password: str
    email_recipient: str
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    # GCP Configuration
    gcp_project_id: str
    gcp_region: str = "us-central1"
    google_application_credentials: Optional[str] = None
    
    # Agent Configuration
    agent_name: str = "Weather Monitor Agent"
    system_prompt: str = "You are a weather monitoring agent that checks daily weather and sends status emails."
    
    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 