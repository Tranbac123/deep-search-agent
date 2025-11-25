"""Naive in-memory rate limiter."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict


@dataclass
class TokenBucket:
    capacity: int
    refill_rate_per_sec: float
    tokens: float = field(init=False)
    last_refill: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        self.tokens = float(self.capacity)

    def consume(self, amount: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate_per_sec)
        self.last_refill = now

        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False


class RateLimiter:
    """Simple per-identifier token bucket limiter."""

    def __init__(self, per_minute: int) -> None:
        self.per_minute = per_minute
        self._buckets: Dict[str, TokenBucket] = {}

    def allow(self, identifier: str) -> bool:
        bucket = self._buckets.get(identifier)
        if bucket is None:
            bucket = TokenBucket(capacity=self.per_minute, refill_rate_per_sec=self.per_minute / 60)
            self._buckets[identifier] = bucket
        return bucket.consume()

    def wrap(self, identifier_provider: Callable[[], str]) -> Callable[[Callable[..., object]], Callable[..., object]]:
        def decorator(fn: Callable[..., object]) -> Callable[..., object]:
            def wrapper(*args, **kwargs):
                identifier = identifier_provider()
                if not self.allow(identifier):
                    raise RuntimeError("Rate limit exceeded")
                return fn(*args, **kwargs)

            return wrapper

        return decorator
