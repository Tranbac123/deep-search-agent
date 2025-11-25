"""Timing helpers."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def timed(section: str) -> Iterator[float]:
    start = time.time()
    try:
        yield start
    finally:
        duration = time.time() - start
        print(f"[Timing] {section}: {duration:.2f}s")
