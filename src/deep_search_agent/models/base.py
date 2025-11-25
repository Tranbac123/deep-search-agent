"""Interfaces for language model backends."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class LLMResponse:
    text: str


class BaseLLM(Protocol):
    """Minimal interface consumed by workflows."""

    def generate(self, prompt: str) -> LLMResponse:
        ...

    def chat(self, messages: List[ChatMessage]) -> LLMResponse:
        ...
