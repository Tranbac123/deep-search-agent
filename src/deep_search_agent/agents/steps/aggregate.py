"""Aggregate raw documents into a bullet list."""

from __future__ import annotations

from typing import Iterable, List

from ...retrieval.base import WebDocument
from ...utils.text import truncate_paragraph


def aggregate_docs(documents: Iterable[WebDocument]) -> List[str]:
    bullets: List[str] = []
    for doc in documents:
        bullets.append(f"[{doc.title}]({doc.url}): {truncate_paragraph(doc.snippet)}")
    return bullets
