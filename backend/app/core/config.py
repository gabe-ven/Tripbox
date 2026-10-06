from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tripbox API"
    environment: str = "development"
    log_level: str = "INFO"
    # Claude rejects images over 5 MB.
    max_upload_bytes: int = 5 * 1024 * 1024
    anthropic_api_key: str = ""
    claude_model: str = "claude-opus-5-5"


settings = Settings()
