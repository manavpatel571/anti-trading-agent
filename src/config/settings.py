from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Anti-Trading Agent"
    ENV: str = "development"
    
    # LLM
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password123@localhost:5432/anti_trading"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Data APIs
    EODHD_API_KEY: str = ""
    FRED_API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
