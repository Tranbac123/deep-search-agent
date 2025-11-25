"""Placeholder for a LangGraph-style workflow.

Implemented as a simple wrapper that internally delegates to the production workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..context.memory import ConversationMemory
from ..models.base import BaseLLM
from ..retrieval.base import BaseRetriever
from .production import ProductionWorkflow

if TYPE_CHECKING:
    from ..agents.deep_search_agent import AgentResult


@dataclass
class LangGraphWorkflow:
    llm: BaseLLM
    retriever: BaseRetriever

    def __post_init__(self) -> None:
        self._delegate = ProductionWorkflow(llm=self.llm, retriever=self.retriever)

    def run(self, query: str, memory: ConversationMemory) -> "AgentResult":
        return self._delegate.run(query, memory)
