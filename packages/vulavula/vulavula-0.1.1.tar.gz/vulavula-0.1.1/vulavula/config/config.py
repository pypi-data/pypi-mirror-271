from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str = "https://beta-vulavula-services.lelapa.ai/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
