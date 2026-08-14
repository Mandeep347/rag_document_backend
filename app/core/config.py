from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    cohere_api_key: str
    database_url: str
    jwt_secret: str
    expire_time: int
    algorithm: str
    #redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    supabase_url: str
    supabase_key: str
    supabase_bucket: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()