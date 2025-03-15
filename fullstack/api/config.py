from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str
    ollama_generate_path: str


settings = Settings()
