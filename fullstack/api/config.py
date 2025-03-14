from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_url: str


settings = Settings()
