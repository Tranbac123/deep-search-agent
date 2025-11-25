"""Search helper."""

from __future__ import annotations

from typing import List

from ...retrieval.base import BaseRetriever, WebDocument


def search_web(query: str, retriever: BaseRetriever, per_query_results: int = 3) -> List[WebDocument]:
    return retriever.search(query, max_results=per_query_results)
