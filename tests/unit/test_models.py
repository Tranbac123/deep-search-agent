from deep_search_agent.models.base import ChatMessage
from deep_search_agent.models.local_backend import LocalLLM


def test_local_llm_generate() -> None:
    llm = LocalLLM(seed=1)
    response = llm.generate("Hello world")
    assert "Synthesized answer" in response.text


def test_local_llm_chat() -> None:
    llm = LocalLLM(seed=2)
    response = llm.chat([ChatMessage(role="user", content="Hi"), ChatMessage(role="assistant", content="Hello")])
    assert "Synthesized answer" in response.text
