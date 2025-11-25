"""Tool wrapper around the Retriever."""

from __future__ import annotations

from typing import List

from ..retrieval.base import BaseRetriever, WebDocument


class WebSearchTool:
    def __init__(self, retriever: BaseRetriever) -> None:
        self.retriever = retriever

    def __call__(self, query: str, limit: int = 5) -> List[WebDocument]:
        return self.retriever.search(query, max_results=limit)
