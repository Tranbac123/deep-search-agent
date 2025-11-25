from dataclasses import dataclass
from typing import List

from deep_search_agent.agents.types import AgentResult, ResearchFinding
from deep_search_agent.agents.deep_search_agent import DeepSearchAgent, AgentDependencies
from deep_search_agent.context.memory import ConversationMemory
from deep_search_agent.models.base import BaseLLM, ChatMessage, LLMResponse
from deep_search_agent.retrieval.base import BaseRetriever, WebDocument
from deep_search_agent.workflows.basic import BasicWorkflow


class StubLLM(BaseLLM):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt: str) -> LLMResponse:
        self.calls += 1
        return LLMResponse(text="bullet\nbullet2")

    def chat(self, messages: List[ChatMessage]) -> LLMResponse:
        return self.generate(messages[-1].content)


class StubRetriever(BaseRetriever):
    def search(self, query: str, max_results: int = 5) -> List[WebDocument]:
        return [
            WebDocument(title="Result", url="https://example.com", snippet="python web framework", content=""),
        ]


def test_agent_run_returns_result() -> None:
    llm = StubLLM()
    retriever = StubRetriever()
    workflow = BasicWorkflow(llm=llm, retriever=retriever)
    agent = DeepSearchAgent(AgentDependencies(llm=llm, retriever=retriever))
    agent.workflow = workflow
    result = agent.run("python web frameworks")
    assert result.summary
    assert llm.calls >= 1
