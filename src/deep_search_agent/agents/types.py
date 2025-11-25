"""Shared types for agent results and findings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ResearchFinding:
    title: str
    url: str
    snippet: str

    def to_dict(self) -> dict:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


@dataclass
class AgentResult:
    query: str
    plan: List[str]
    findings: List[ResearchFinding]
    summary: str

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "plan": self.plan,
            "answer": self.summary,
            "sources": [finding.to_dict() for finding in self.findings],
        }

