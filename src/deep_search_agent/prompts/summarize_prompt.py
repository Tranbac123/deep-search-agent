"""Prompt for final synthesis."""

SUMMARY_TEMPLATE = """Synthesize a final answer for the query below.
Use bullet points, cite sources by number when possible, and end with a short verdict.

Question: {query}
Key findings:
{findings}
"""
