from pydantic import BaseSettings, Field
from functools import lru_cache


class LLMSettings(BaseSettings):
    openai_api_key: str = Field(None, env="OPENAI_API_KEY")
    model: str = Field("gpt-4o", env="LLM_MODEL")
    temperature: float = Field(0.1, env="LLM_TEMPERATURE")
    max_tokens: int | None = Field(None, env="LLM_MAX_TOKENS")


class FirecrawlSettings(BaseSettings):
    api_key: str | None = Field(None, env="FIRECRAWL_API_KEY")
    timeout_ms: int = Field(15000, env="FIRECRAWL_TIMEOUT")
    max_results: int = Field(10, env="FIRECRAWL_MAX_RESULTS")


class SearchProviderSettings(BaseSettings):
    tavily_api_key: str | None = Field(None, env="TAVILY_API_KEY")
    brave_api_key: str | None = Field(None, env="BRAVE_API_KEY")


class EmbeddingSettings(BaseSettings):
    model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL_NAME")
    device: str | None = Field(None, env="EMBEDDING_DEVICE")
    batch_size: int = Field(16, env="EMBEDDING_BATCH_SIZE")
    rag_top_k: int = Field(6, env="RAG_TOP_K")
    similarity_threshold: float = Field(0.35, env="VECTOR_SIMILARITY_THRESHOLD")
    vector_store_dir: str = Field(".vector_store", env="VECTOR_STORE_DIR")


class WorkflowSettings(BaseSettings):
    max_tools_per_query: int = Field(5, env="MAX_TOOLS_PER_QUERY")
    max_content_length: int = Field(2000, env="MAX_CONTENT_LENGTH")


class RateLimitSettings(BaseSettings):
    enable_rate_limit: bool = Field(True, env="ENABLE_RATE_LIMITING")
    requests_per_minute: int = Field(60, env="REQUESTS_PER_MINUTE")
    max_concurrent_requests: int = Field(5, env="MAX_CONCURRENT_REQUESTS")


class CacheSettings(BaseSettings):
    enable_cache: bool = Field(True, env="ENABLE_CACHING")
    ttl_hours: int = Field(24, env="CACHE_TTL_HOURS")
    redis_url: str | None = Field(None, env="REDIS_URL")


class LoggingSettings(BaseSettings):
    level: str = Field("INFO", env="LOG_LEVEL")
    format: str = Field("json", env="LOG_FORMAT")


class MonitoringSettings(BaseSettings):
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    prometheus_port: int = Field(8000, env="PROMETHEUS_PORT")


class DatabaseSettings(BaseSettings):
    url: str | None = Field(None, env="DATABASE_URL")


# =============================
# Deep Search Agent Settings
# =============================

class DeepSearchLLMSettings(BaseSettings):
    provider: str = Field("local", env="DEEPSEARCH_LLM_PROVIDER")  # "openai" or "local"
    offline: bool = Field(True, env="DEEPSEARCH_OFFLINE")

    # Only required if provider="openai"
    openai_model: str | None = Field(None, env="OPENAI_MODEL")
    openai_temperature: float | None = Field(None, env="OPENAI_TEMPERATURE")


class DeepSearchRetrievalSettings(BaseSettings):
    web_max_results: int = Field(5, env="WEB_MAX_RESULTS")
    rag_top_k: int = Field(3, env="DEEPSEARCH_RAG_TOP_K")


class DeepSearchPerformanceSettings(BaseSettings):
    enable_agent_cache: bool = Field(True, env="ENABLE_AGENT_CACHE")
    cache_ttl_seconds: int = Field(600, env="CACHE_TTL_SECONDS")
    rate_limit_per_minute: int = Field(30, env="RATE_LIMIT_PER_MINUTE")
    user_agent: str = Field("DeepSearchAgent/1.0", env="DEEPSEARCH_USER_AGENT")
    crawler_timeout: float = Field(10.0, env="CRAWLER_TIMEOUT")


# ============================================================
# Global Settings Aggregator (the one you import everywhere)
# ============================================================

class Settings(BaseSettings):
    llm: LLMSettings = LLMSettings()
    firecrawl: FirecrawlSettings = FirecrawlSettings()
    search_providers: SearchProviderSettings = SearchProviderSettings()
    embedding: EmbeddingSettings = EmbeddingSettings()
    workflow: WorkflowSettings = WorkflowSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    cache: CacheSettings = CacheSettings()
    logging: LoggingSettings = LoggingSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    database: DatabaseSettings = DatabaseSettings()

    deep_llm: DeepSearchLLMSettings = DeepSearchLLMSettings()
    deep_retrieval: DeepSearchRetrievalSettings = DeepSearchRetrievalSettings()
    deep_perf: DeepSearchPerformanceSettings = DeepSearchPerformanceSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global instance
settings = get_settings()
