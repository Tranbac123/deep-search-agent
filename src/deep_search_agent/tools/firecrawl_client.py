"""Wrapper exposing the crawler as a tool-like interface."""

from __future__ import annotations

from ..retrieval.crawler import SimpleCrawler


class FirecrawlTool:
    """Named after the real service, but uses SimpleCrawler for demo purposes."""

    def __init__(self) -> None:
        self.crawler = SimpleCrawler()

    def __call__(self, url: str) -> str:
        return self.crawler.fetch(url)
