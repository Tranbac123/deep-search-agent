"""Thin wrapper around the OpenAI client."""

from __future__ import annotations

from typing import List, Optional

from openai import OpenAI

from ..config import settings
from .base import BaseLLM, ChatMessage, LLMResponse


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> None:
        key = api_key or settings.openai_api_key
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI backend")
        self.client = OpenAI(api_key=key)
        self.model = model or settings.openai_model
        self.temperature = temperature if temperature is not None else settings.openai_temperature

    def generate(self, prompt: str) -> LLMResponse:
        completion = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=self.temperature,
        )
        return LLMResponse(text=completion.output[0].content[0].text)

    def chat(self, messages: List[ChatMessage]) -> LLMResponse:
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[message.__dict__ for message in messages],
        )
        return LLMResponse(text=completion.choices[0].message.content or "")
