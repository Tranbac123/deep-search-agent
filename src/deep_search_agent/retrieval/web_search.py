"""DuckDuckGo-based web search retriever."""

from __future__ import annotations

from html.parser import HTMLParser
from typing import List, Optional
from urllib.parse import quote_plus

import httpx

from ..config import settings
from ..infra.cache import TTLCache
from ..infra.logger import get_logger
from .base import BaseRetriever, WebDocument


logger = get_logger(__name__)


class _DuckDuckGoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._results: List[WebDocument] = []
        self._capture = False
        self._current_url: Optional[str] = None
        self._current_title: Optional[str] = None
        self._current_snippet: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("http"):
                self._capture = True
                self._current_url = href
                self._current_title = ""
                self._current_snippet = []

    def handle_endtag(self, tag):
        if tag == "a" and self._capture:
            snippet = " ".join(self._current_snippet).strip()
            doc = WebDocument(
                title=(self._current_title or "").strip(),
                url=self._current_url or "",
                snippet=snippet[:180],
                content=snippet,
            )
            self._results.append(doc)
            self._capture = False

    def handle_data(self, data):
        if not self._capture:
            return
        if self._current_title == "":
            self._current_title = data.strip()
        else:
            self._current_snippet.append(data.strip())

    def results(self) -> List[WebDocument]:
        return self._results


class DuckDuckGoRetriever(BaseRetriever):
    """Lightweight retriever that scrapes DuckDuckGo Lite results."""

    def __init__(self, max_results: int = 5) -> None:
        self.max_results = max_results
        self.client = httpx.Client(timeout=10.0, headers={"User-Agent": settings.user_agent})
        self.cache = TTLCache[str, List[WebDocument]](ttl_seconds=settings.cache_ttl_seconds)

    def search(self, query: str, max_results: Optional[int] = None) -> List[WebDocument]:
        target = max_results or self.max_results
        cached = self.cache.get(query)
        if cached:
            return cached[:target]

        url = f"https://duckduckgo.com/lite/?q={quote_plus(query)}"
        logger.debug("Fetching search results", extra={"url": url})
        response = self.client.get(url)
        response.raise_for_status()

        parser = _DuckDuckGoParser()
        parser.feed(response.text)

        results = [doc for doc in parser.results() if doc.url][:target]
        if not results:
            fallback = WebDocument(
                title=f"Result for {query}",
                url="https://duckduckgo.com/",
                snippet="DuckDuckGo search result placeholder.",
                content=response.text[:400],
            )
            results = [fallback]

        self.cache.set(query, results)
        return results
