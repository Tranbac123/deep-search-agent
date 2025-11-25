"""Utility helpers for working with text."""

from __future__ import annotations

import re
from textwrap import shorten, wrap
from typing import Iterable, List


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def truncate_paragraph(value: str, max_chars: int = 280) -> str:
    return shorten(normalize_whitespace(value), width=max_chars, placeholder="…")


def bullet_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {normalize_whitespace(item)}" for item in items if item)


def wrap_text(value: str, width: int = 80) -> str:
    return "\n".join(wrap(normalize_whitespace(value), width=width))
