"""Prompt templates for planning web searches."""

PLAN_TEMPLATE = """Question: {query}

Generate 3 focused sub-questions that would help answer the question.
Return them as a numbered list."""


AGGREGATION_TEMPLATE = """You are given raw web snippets. Summarize the key
facts and list any concrete data points. Keep the output concise.

Question: {query}
Snippets:
{snippets}
"""
