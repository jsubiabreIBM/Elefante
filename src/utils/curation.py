"""Deterministic curation helpers (no LLMs).

These utilities are used to ensure memories have reasonable `title` and `summary`
fields at ingestion time and during batch backfills.

Keep these functions cheap, stable, and side-effect free.
"""

from __future__ import annotations

import re
from typing import Optional


_CODEBLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def collapse_ws(text: str) -> str:
    return " ".join((text or "").split()).strip()


def strip_codeblocks(text: str) -> str:
    return _CODEBLOCK_RE.sub(" ", text or "")


def first_sentence(text: str) -> str:
    text = collapse_ws(text)
    if not text:
        return ""
    text = text.replace("- ", "").replace("* ", "")
    parts = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    return (parts[0] if parts else text).strip()


def truncate(text: str, max_len: int) -> str:
    text = collapse_ws(text)
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rstrip()
    return cut + "…"


def generate_title(
    *,
    content: str,
    layer: Optional[str],
    sublayer: Optional[str],
    max_len: int = 90,
) -> str:
    cleaned = strip_codeblocks(content or "")
    cleaned = collapse_ws(cleaned)

    words = cleaned.split()
    core = " ".join(words[:10]) if words else "Memory"
    core = truncate(core, 70)

    l = (layer or "world").strip() or "world"
    s = (sublayer or "fact").strip() or "fact"

    title = f"{l}.{s}: {core}" if core else f"{l}.{s}: Memory"
    return truncate(title, max_len) or "Memory"


def generate_summary(*, content: str, max_len: int = 200) -> str:
    cleaned = strip_codeblocks(content or "")
    s = first_sentence(cleaned)
    if not s:
        s = collapse_ws(cleaned)
    return truncate(s, max_len) or ""
