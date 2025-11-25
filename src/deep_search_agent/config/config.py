"""Runtime configuration for the Deep Search Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """Container for all configurable runtime values."""

    llm_provider: str
    openai_api_key: Optional[str]
    openai_model: str
    openai_temperature: float
    web_max_results: int
    rag_top_k: int
    enable_cache: bool
    cache_ttl_seconds: int
    rate_limit_per_minute: int
    user_agent: str
    crawler_timeout: float
    offline: bool

    def with_overrides(self, **kwargs) -> "Settings":
        return replace(self, **kwargs)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings from environment variables with sensible defaults."""

    return Settings(
        llm_provider=os.getenv("DEEPSEARCH_LLM_PROVIDER", "local").lower(),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
        web_max_results=int(os.getenv("WEB_MAX_RESULTS", "5")),
        rag_top_k=int(os.getenv("RAG_TOP_K", "3")),
        enable_cache=os.getenv("ENABLE_AGENT_CACHE", "true").lower() == "true",
        cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "600")),
        rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "30")),
        user_agent=os.getenv("DEEPSEARCH_USER_AGENT", "DeepSearchAgent/1.0"),
        crawler_timeout=float(os.getenv("CRAWLER_TIMEOUT", "10.0")),
        offline=os.getenv("DEEPSEARCH_OFFLINE", "false").lower() == "true",
    )


settings = get_settings()
