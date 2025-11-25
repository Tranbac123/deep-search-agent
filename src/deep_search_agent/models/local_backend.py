"""Local deterministic LLM used for offline/demo scenarios."""

from __future__ import annotations

import random
from textwrap import dedent
from typing import List

from .base import BaseLLM, ChatMessage, LLMResponse


class LocalLLM(BaseLLM):
    """A pragmatic stub model that produces deterministic but useful text."""

    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)

    def generate(self, prompt: str) -> LLMResponse:
        summary = "\n".join(line.strip() for line in prompt.splitlines() if line.strip())[-380:]
        text = dedent(
            f"""
            Synthesized answer:
            {summary}
            Key takeaways:
            - This is a heuristic summary for offline usage.
            - Replace LocalLLM with OpenAI backend for higher quality.
            """
        ).strip()
        return LLMResponse(text=text)

    def chat(self, messages: List[ChatMessage]) -> LLMResponse:
        compiled = "\n".join(f"{m.role.upper()}: {m.content}" for m in messages)
        return self.generate(compiled)
