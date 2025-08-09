from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = "dev"
    APP_NAME: str = "BizPilot"
    SECRET_KEY: str = Field(default="change-me")
    OPENAI_API_KEY: str | None = None

    POSTGRES_USER: str = "bizpilot"
    POSTGRES_PASSWORD: str = "bizpilot"
    POSTGRES_DB: str = "bizpilot"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://redis:6379/0"
    VECTOR_PROVIDER: str = "pgvector"
    EMBEDDINGS_MODEL: str = "text-embedding-3-large"

    EMAIL_SMTP_HOST: str | None = None
    EMAIL_SMTP_PORT: int | None = 587
    EMAIL_SMTP_USER: str | None = None
    EMAIL_SMTP_PASS: str | None = None
    EMAIL_FROM: str | None = None

    # connectors will extend these at runtime if present
    SHOPIFY_STORE_DOMAIN: str | None = None
    SHOPIFY_ADMIN_TOKEN: str | None = None
    SHOPIFY_API_VERSION: str | None = None
    SHOPIFY_WEBHOOK_SECRET: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
