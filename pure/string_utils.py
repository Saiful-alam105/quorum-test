"""Pure-Python string utilities.

This PR is intended to demonstrate Quorum's Python analysis and test
generation. No tests are included here so that Quorum can generate them.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional

_WORD_RE = re.compile(r"[a-z0-9]+")


def slugify(text: str) -> str:
    """Convert *text* into a URL-safe lowercase slug."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    words = _WORD_RE.findall(ascii_text.lower())
    return "-".join(words)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate *text* to *max_length* characters, appending *suffix*."""
    if max_length < len(suffix):
        raise ValueError("max_length must be at least the suffix length")
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Replace runs of whitespace with a single space and trim edges."""
    return " ".join(text.split())


def strip_control_characters(text: str) -> str:
    """Remove non-printable control characters from *text*."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cc")


def count_words(text: str) -> int:
    """Return the number of words in *text*."""
    return len(_WORD_RE.findall(text.lower()))


def is_valid_identifier(value: str) -> bool:
    """Return True when *value* is a valid Python-style identifier."""
    if not value:
        return False
    if not (value[0].isalpha() or value[0] == "_"):
        return False
    return all(ch.isalnum() or ch == "_" for ch in value)


def normalize_filename(filename: str) -> str:
    """Normalize *filename* to lowercase with spaces replaced by dashes."""
    base = unicodedata.normalize("NFKD", filename)
    ascii_base = base.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9.\-]", "-", ascii_base)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned.lower()


def ensure_prefix(text: str, prefix: str) -> str:
    """Return *text* with *prefix* prepended when it is not already there."""
    return text if text.startswith(prefix) else prefix + text


def ensure_suffix(text: str, suffix: str) -> str:
    """Return *text* with *suffix* appended when it is not already there."""
    return text if text.endswith(suffix) else text + suffix


def remove_prefix(text: str, prefix: str) -> str:
    """Remove *prefix* from *text* when present, otherwise return *text*."""
    return text[len(prefix):] if text.startswith(prefix) else text


def remove_suffix(text: str, suffix: str) -> str:
    """Remove *suffix* from *text* when present, otherwise return *text*."""
    return text[: -len(suffix)] if text.endswith(suffix) else text


def split_words(text: str) -> List[str]:
    """Split *text* into lowercase words, ignoring punctuation."""
    return _WORD_RE.findall(text.lower())


def mask_string(value: str, visible: int = 4, mask_char: str = "*") -> str:
    """Mask *value* keeping the last *visible* characters visible."""
    if visible < 0:
        raise ValueError("visible must not be negative")
    if len(value) <= visible:
        return value
    return mask_char * (len(value) - visible) + value[-visible:]


def to_title_case(text: str) -> str:
    """Convert *text* to Title Case."""
    return text.title()


def lines_to_list(text: str, strip_blank: bool = False) -> List[str]:
    """Split *text* into a list of lines, optionally dropping blanks."""
    lines = text.splitlines()
    if strip_blank:
        return [line for line in lines if line.strip()]
    return lines


if __name__ == "__main__":
    print(slugify("Hello, World! This Is A Demo."))