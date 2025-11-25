"""Core agent exposed to CLI and other entrypoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .types import AgentResult, ResearchFinding
from ..config import Settings, settings
from ..context.memory import ConversationMemory
from ..models.base import BaseLLM
from ..models.local_backend import LocalLLM
from ..models.openai_backend import OpenAILLM
from ..retrieval.base import BaseRetriever
from ..retrieval.stub import StubRetriever
from ..retrieval.web_search import DuckDuckGoRetriever

if TYPE_CHECKING:
    from ..workflows.langgraph_based import LangGraphWorkflow
    from ..workflows.basic import BasicWorkflow
    from ..workflows.production import ProductionWorkflow


@dataclass
class AgentDependencies:
    llm: BaseLLM
    retriever: BaseRetriever
    workflow_name: str = "basic"


class DeepSearchAgent:
    """High-level façade coordinating workflows and dependencies."""

    def __init__(self, deps: AgentDependencies) -> None:
        self.deps = deps
        self.memory = ConversationMemory()
        self.workflow = self._build_workflow(deps.workflow_name)

    def _build_workflow(self, name: str):
        if name == "production":
            from ..workflows.production import ProductionWorkflow
            return ProductionWorkflow(llm=self.deps.llm, retriever=self.deps.retriever)
        if name == "langgraph":
            from ..workflows.langgraph_based import LangGraphWorkflow
            return LangGraphWorkflow(llm=self.deps.llm, retriever=self.deps.retriever)
        from ..workflows.basic import BasicWorkflow
        return BasicWorkflow(llm=self.deps.llm, retriever=self.deps.retriever)

    def run(self, query: str) -> AgentResult:
        result = self.workflow.run(query, memory=self.memory)
        self.memory.add(query, result.summary)
        return result

    @classmethod
    def from_settings(cls, settings_obj: Settings, *, workflow_name: str = "basic") -> "DeepSearchAgent":
        """Factory for embedding into SmartBuyer or other hosts.

        Example:
            from deep_search_agent.config import get_settings
            from deep_search_agent.agents.deep_search_agent import DeepSearchAgent

            settings = get_settings()
            agent = DeepSearchAgent.from_settings(settings, workflow_name="production")
            result = agent.run("best LLM frameworks 2024")
        """

        llm = _build_llm(settings_obj)
        retriever = _build_retriever(settings_obj)
        deps = AgentDependencies(llm=llm, retriever=retriever, workflow_name=workflow_name)
        return cls(deps)

def default_agent(llm: BaseLLM, retriever: BaseRetriever | None = None, workflow: str = "basic") -> DeepSearchAgent:
    retriever = retriever or DuckDuckGoRetriever(max_results=settings.web_max_results)
    deps = AgentDependencies(llm=llm, retriever=retriever, workflow_name=workflow)
    return DeepSearchAgent(deps)


def _build_llm(settings_obj: Settings) -> BaseLLM:
    if settings_obj.offline or settings_obj.llm_provider != "openai":
        return LocalLLM()
    if not settings_obj.openai_api_key:
        return LocalLLM()
    return OpenAILLM(api_key=settings_obj.openai_api_key, model=settings_obj.openai_model)


def _build_retriever(settings_obj: Settings) -> BaseRetriever:
    if settings_obj.offline:
        return StubRetriever()
    return DuckDuckGoRetriever(max_results=settings_obj.web_max_results)
