from pydantic_settings import BaseSettings, SettingsConfigDict

class BrokerSettings(BaseSettings):
    ZERODHA_API_KEY: str = ""
    ZERODHA_API_SECRET: str = ""
    ZERODHA_USER_ID: str = ""
    ZERODHA_TOTP_SECRET: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

broker_settings = BrokerSettings()
