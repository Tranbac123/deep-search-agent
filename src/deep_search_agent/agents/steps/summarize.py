"""Summarization helper."""

from __future__ import annotations

from typing import Iterable

from ...models.base import BaseLLM
from ...prompts import summarize_prompt


def summarize_findings(query: str, findings: Iterable[str], llm: BaseLLM) -> str:
    prompt = summarize_prompt.SUMMARY_TEMPLATE.format(query=query, findings="\n".join(findings))
    return llm.generate(prompt).text
