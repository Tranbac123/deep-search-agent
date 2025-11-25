"""Interfaces for search / crawling components."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class WebDocument:
    title: str
    url: str
    snippet: str
    content: str


class BaseRetriever(Protocol):
    def search(self, query: str, max_results: int = 5) -> List[WebDocument]:
        ...
