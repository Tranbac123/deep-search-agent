"""Lightweight semantic ranking for retrieved snippets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .base import WebDocument


@dataclass
class RankedDocument:
    document: WebDocument
    score: float


def score_documents(query: str, documents: List[WebDocument]) -> List[RankedDocument]:
    query_terms = set(query.lower().split())
    ranked: List[RankedDocument] = []
    for doc in documents:
        snippet_terms = set(doc.snippet.lower().split())
        overlap = len(query_terms & snippet_terms)
        score = overlap / max(len(query_terms), 1)
        ranked.append(RankedDocument(document=doc, score=score))
    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked
