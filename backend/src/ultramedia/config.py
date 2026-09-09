from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "UltraMedia Studio API"
    environment: str = "development"
    database_url: str = "sqlite:///./ultramedia.db"
    cors_origins: str = "http://localhost:3000,https://ultramedia-studio.siva-babu.chatgpt.site"
    approval_api_key: str | None = None

    provider_mode: str = "auto"
    fireworks_api_key: str | None = None
    fireworks_chat_model: str = "accounts/fireworks/models/qwen3p7-plus"
    fireworks_embedding_model: str = "accounts/fireworks/models/qwen3-embedding-8b"
    fireworks_rerank_model: str = "accounts/fireworks/models/qwen3-reranker-8b"
    embedding_dimensions: int = 256

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b-instruct"
    llamacpp_base_url: str = "http://127.0.0.1:8080"
    llamacpp_model: str = "qwen3:4b-instruct"
    generation_max_tokens: int = 1024

    mistral_api_key: str | None = None
    mistral_model: str = "mistral-small-latest"
    langsmith_api_key: str | None = None
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_project: str = "ultramedia-production"
    otel_exporter_otlp_endpoint: str | None = None

    pinecone_api_key: str | None = None
    pinecone_index_host: str | None = None
    pinecone_namespace: str = "ultramedia-public-v1"

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", "../.env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def data_dir(self) -> Path:
        return Path(__file__).resolve().parents[2] / "data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
