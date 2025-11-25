"""Offline stub retriever returning canned results."""

from __future__ import annotations

from typing import List

from .base import BaseRetriever, WebDocument


class StubRetriever(BaseRetriever):
    """Provides deterministic documents for offline mode and tests."""

    def __init__(self) -> None:
        self._docs: List[WebDocument] = [
            WebDocument(
                title="Open-Source Python Frameworks",
                url="https://example.com/python-frameworks",
                snippet="Comparison of Django, FastAPI, and Flask for rapid API development.",
                content="Django offers batteries-included features, FastAPI provides async speed, Flask stays minimal.",
            ),
            WebDocument(
                title="AI Research Trends 2024",
                url="https://example.com/ai-trends",
                snippet="Multi-agent systems and retrieval-augmented generation dominate industry roadmaps.",
                content="Companies invest in agents that plan, retrieve context, and verify outputs.",
            ),
        ]

    def search(self, query: str, max_results: int = 5) -> List[WebDocument]:
        return self._docs[:max_results]

