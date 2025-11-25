"""Simple conversation memory for CLI usage."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, List, Tuple


HistoryItem = Tuple[str, str]


@dataclass
class ConversationMemory:
    max_items: int = 5
    _items: Deque[HistoryItem] = field(default_factory=deque)

    def add(self, query: str, answer: str) -> None:
        self._items.append((query, answer))
        while len(self._items) > self.max_items:
            self._items.popleft()

    def as_bullets(self) -> List[str]:
        return [f"Q: {q}\nA: {a}" for q, a in reversed(self._items)]
