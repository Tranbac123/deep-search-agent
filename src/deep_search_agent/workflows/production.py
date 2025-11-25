"""Production workflow with memory-awareness and deduplication."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from ..agents.types import AgentResult, ResearchFinding
from ..context.memory import ConversationMemory
from ..models.base import BaseLLM
from ..retrieval.base import BaseRetriever, WebDocument
from ..retrieval.rag import score_documents
from ..utils.text import normalize_whitespace
from .basic import BasicWorkflow


def deduplicate_docs(documents: List[WebDocument]) -> List[WebDocument]:
    seen: Set[str] = set()
    unique: List[WebDocument] = []
    for doc in documents:
        key = normalize_whitespace(doc.url or doc.title)
        if key in seen:
            continue
        seen.add(key)
        unique.append(doc)
    return unique


@dataclass
class ProductionWorkflow(BasicWorkflow):
    """Extends the basic workflow with deduplication and memory context."""

    def run(self, query: str, memory: ConversationMemory) -> AgentResult:
        base_result = super().run(query, memory)
        deduped_findings = deduplicate_docs(
            [
                WebDocument(
                    title=finding.title,
                    url=finding.url,
                    snippet=finding.snippet,
                    content=finding.snippet,
                )
                for finding in base_result.findings
            ]
        )
        ranked = score_documents(query, deduped_findings)
        findings = [
            ResearchFinding(title=rank.document.title, url=rank.document.url, snippet=rank.document.snippet)
            for rank in ranked
        ]
        return AgentResult(query=base_result.query, plan=base_result.plan, findings=findings, summary=base_result.summary)
