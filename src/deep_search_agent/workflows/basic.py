"""Basic workflow: plan -> search -> aggregate -> summarize."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..agents.types import AgentResult, ResearchFinding
from ..agents.steps.aggregate import aggregate_docs
from ..agents.steps.plan import create_plan
from ..agents.steps.search import search_web
from ..agents.steps.summarize import summarize_findings
from ..context.memory import ConversationMemory
from ..models.base import BaseLLM
from ..retrieval.base import BaseRetriever
from ..retrieval.rag import score_documents


@dataclass
class BasicWorkflow:
    llm: BaseLLM
    retriever: BaseRetriever
    per_subquery_results: int = 3

    def run(self, query: str, memory: ConversationMemory) -> AgentResult:
        plan = create_plan(query, self.llm) or [query]
        documents = []
        for step in plan:
            documents.extend(search_web(step, self.retriever, self.per_subquery_results))

        ranked = score_documents(query, documents)[:5]
        findings = [
            ResearchFinding(title=rank.document.title, url=rank.document.url, snippet=rank.document.snippet)
            for rank in ranked
        ]

        aggregated = aggregate_docs(documents)
        summary = summarize_findings(query, aggregated, self.llm)

        return AgentResult(query=query, plan=plan, findings=findings, summary=summary)
