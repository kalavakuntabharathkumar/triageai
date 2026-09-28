from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./triage.db"
    llm_provider: str = "rules"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
