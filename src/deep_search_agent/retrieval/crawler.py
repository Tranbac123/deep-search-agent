"""Very small crawler used to fetch article bodies."""

from __future__ import annotations

import httpx

from ..config import settings
from ..infra.cache import TTLCache
from ..infra.logger import get_logger


logger = get_logger(__name__)


class SimpleCrawler:
    def __init__(self) -> None:
        self.client = httpx.Client(timeout=settings.crawler_timeout, headers={"User-Agent": settings.user_agent})
        self.cache = TTLCache[str, str](ttl_seconds=settings.cache_ttl_seconds)

    def fetch(self, url: str) -> str:
        cached = self.cache.get(url)
        if cached:
            return cached
        logger.debug("Crawling url", extra={"url": url})
        response = self.client.get(url)
        response.raise_for_status()
        text = response.text
        self.cache.set(url, text)
        return text
