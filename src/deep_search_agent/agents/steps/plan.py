"""Planning helpers."""

from __future__ import annotations

from typing import List

from ...prompts import search_prompt
from ...models.base import BaseLLM, ChatMessage


def create_plan(query: str, llm: BaseLLM) -> List[str]:
    """Ask the LLM (or heuristic) to propose sub-questions."""

    prompt = search_prompt.PLAN_TEMPLATE.format(query=query)
    response = llm.generate(prompt)
    return [line.strip().lstrip("-1234567890. ").strip() for line in response.text.splitlines() if line.strip()]
