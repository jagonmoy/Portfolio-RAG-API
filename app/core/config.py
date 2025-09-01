from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    github_token: str = ""
    log_level: str = "INFO"
    chroma_persist_path: str = "./data/storage/chroma_db"
    max_response_time: int = 3

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
