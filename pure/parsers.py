"""Pure-Python CSV/data parsing helpers.

This PR is intended to demonstrate Quorum's Python analysis and test
generation. No tests are included here so that Quorum can generate them.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence


@dataclass
class ParseResult:
    """Outcome of parsing one CSV row."""

    values: List[str] = field(default_factory=list)
    ok: bool = True
    error: Optional[str] = None


def parse_row(line: str, delimiter: str = ",") -> ParseResult:
    """Parse a single CSV *line* into fields.

    Handles empty fields, whitespace and quoted values. Returns a
    :class:`ParseResult` with ``ok=False`` on malformed input.
    """
    if "\n" in line:
        return ParseResult(ok=False, error="single line expected")
    reader = csv.reader([line], delimiter=delimiter)
    try:
        row = next(reader)
    except csv.Error as exc:
        return ParseResult(ok=False, error=str(exc))
    return ParseResult(values=list(row))


def parse_rows(text: str, delimiter: str = ",") -> List[ParseResult]:
    """Parse multi-line *text* into a list of :class:`ParseResult`."""
    results: List[ParseResult] = []
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    try:
        for row in reader:
            results.append(ParseResult(values=list(row)))
    except csv.Error as exc:
        results.append(ParseResult(ok=False, error=str(exc)))
    return results


def clean_field(value: str) -> str:
    """Strip surrounding whitespace from a single CSV field."""
    return value.strip()


def to_int(value: str, default: Optional[int] = None) -> Optional[int]:
    """Convert *value* to an int, returning *default* on failure."""
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return default


def to_float(value: str, default: Optional[float] = None) -> Optional[float]:
    """Convert *value* to a float, returning *default* on failure."""
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return default


def parse_int_columns(
    rows: Iterable[Sequence[str]], column_index: int, default: Optional[int] = None
) -> List[Optional[int]]:
    """Convert *column_index* of every row in *rows* to ints."""
    return [
        to_int(row[column_index], default)
        if column_index < len(row)
        else default
        for row in rows
    ]


def strip_all_fields(row: Sequence[str]) -> List[str]:
    """Return *row* with every field trimmed of surrounding whitespace."""
    return [clean_field(field) for field in row]


def drop_empty_rows(rows: Iterable[Sequence[str]]) -> List[List[str]]:
    """Return only rows that contain at least one non-blank field."""
    kept: List[List[str]] = []
    for row in rows:
        if any(field.strip() for field in row):
            kept.append(list(row))
    return kept


def parse_headers(text: str, delimiter: str = ",") -> List[str]:
    """Parse the header line of *text* into field names."""
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    try:
        return next(reader)
    except (csv.Error, StopIteration):
        return []


def rows_to_dicts(
    headers: Sequence[str], rows: Iterable[Sequence[str]]
) -> List[Dict[str, str]]:
    """Convert *rows* into dicts keyed by *headers* (short rows are padded)."""
    records: List[Dict[str, str]] = []
    for row in rows:
        record: Dict[str, str] = {}
        for index, header in enumerate(headers):
            record[header] = row[index] if index < len(row) else ""
        records.append(record)
    return records


def unquote(value: str) -> str:
    """Strip surrounding double quotes from *value* if both are present."""
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def parse_optional_field(value: str, default: str = "") -> str:
    """Return *value* stripped, or *default* when blank or ``-``."""
    cleaned = clean_field(value)
    if cleaned in ("", "-"):
        return default
    return cleaned


def split_line(line: str, delimiter: str = ",") -> List[str]:
    """Split *line* on *delimiter*, handling quoted sections."""
    result = parse_row(line, delimiter)
    return result.values


if __name__ == "__main__":
    sample = "name,age,score\nalice,30,92.5\nbob,25,88\n"
    print([r.values for r in parse_rows(sample)])