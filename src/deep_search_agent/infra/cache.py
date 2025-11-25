"""Simple in-memory cache with TTL support."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, Generic, Optional, Tuple, TypeVar


K = TypeVar("K")
V = TypeVar("V")


@dataclass
class CacheEntry(Generic[V]):
    value: V
    expires_at: float


class TTLCache(Generic[K, V]):
    """A tiny cache suitable for demo usage."""

    def __init__(self, ttl_seconds: int = 600) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: Dict[K, CacheEntry[V]] = {}

    def get(self, key: K) -> Optional[V]:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.expires_at < time.time():
            self._store.pop(key, None)
            return None
        return entry.value

    def set(self, key: K, value: V) -> None:
        self._store[key] = CacheEntry(value=value, expires_at=time.time() + self.ttl_seconds)

    def get_or_set(self, key: K, factory: Callable[[], V]) -> V:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.set(key, value)
        return value
