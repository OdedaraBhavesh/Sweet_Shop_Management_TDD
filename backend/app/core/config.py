from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
