from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tripbox API"
    environment: str = "development"
    log_level: str = "INFO"
    max_upload_bytes: int = 10 * 1024 * 1024


settings = Settings()
