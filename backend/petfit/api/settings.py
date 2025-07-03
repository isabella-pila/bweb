import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    postgres_host: str

    docker_env: int  # 1 para Docker, 0 fora

    database_url: str  # asyncpg para FastAPI
    database_url_alembic: str  # psycopg2 para Alembic

    pgadmin_default_email: str
    pgadmin_default_password: str
    pgadmin_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()