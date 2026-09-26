"""Pure-Python field validation helpers.

This PR is intended to demonstrate Quorum's Python analysis and test
generation. No tests are included here so that Quorum can generate them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,20}$")
PHONE_RE = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


class ValidationError(ValueError):
    """Raised when a field fails validation."""


@dataclass
class FieldRule:
    """A named validation rule applied to a form value."""

    name: str
    required: bool = True
    min_length: int = 0
    max_length: Optional[int] = None
    allowed_characters: Optional[str] = None


def validate_email(value: str) -> bool:
    """Return True when *value* looks like a valid email address."""
    if not value or len(value) > 254:
        return False
    return EMAIL_RE.match(value) is not None


def validate_password(value: str, min_length: int = 8) -> bool:
    """Return True when *value* satisfies basic password rules.

    Requires a lowercase letter, an uppercase letter and a digit.
    """
    if len(value) < min_length:
        return False
    has_lower = any(ch.islower() for ch in value)
    has_upper = any(ch.isupper() for ch in value)
    has_digit = any(ch.isdigit() for ch in value)
    return has_lower and has_upper and has_digit


def validate_username(value: str) -> bool:
    """Return True when *value* is an allowed username (3-20 chars)."""
    return USERNAME_RE.match(value) is not None


def validate_phone(value: str) -> bool:
    """Return True when *value* is a plausible phone number."""
    return PHONE_RE.match(value) is not None


def validate_required(value: Optional[str]) -> bool:
    """Return True when *value* is present and not blank."""
    return value is not None and value.strip() != ""


def validate_length(
    value: str, min_length: int = 0, max_length: Optional[int] = None
) -> bool:
    """Return True when *value* length is within ``[min_length, max_length]``."""
    if len(value) < min_length:
        return False
    if max_length is not None and len(value) > max_length:
        return False
    return True


def validate_allowed_characters(value: str, allowed: str) -> bool:
    """Return True when every character in *value* appears in *allowed*."""
    return all(ch in allowed for ch in value)


def validate_positive_integer(value: int) -> bool:
    """Return True when *value* is a positive integer."""
    return isinstance(value, int) and value > 0


def validate_in_range(value: float, low: float, high: float) -> bool:
    """Return True when *value* is within ``[low, high]``."""
    return low <= value <= high


def validate_rule(rule: FieldRule, value: Optional[str]) -> List[str]:
    """Apply *rule* to *value* and return a list of failure messages."""
    errors: List[str] = []
    if rule.required and not validate_required(value):
        errors.append(f"{rule.name} is required")
        return errors
    if value is None:
        return errors
    if rule.min_length and not validate_length(value, rule.min_length):
        errors.append(f"{rule.name} must be at least {rule.min_length} characters")
    if rule.max_length is not None and not validate_length(
        value, 0, rule.max_length
    ):
        errors.append(f"{rule.name} must be at most {rule.max_length} characters")
    if rule.allowed_characters is not None and not validate_allowed_characters(
        value, rule.allowed_characters
    ):
        errors.append(f"{rule.name} contains disallowed characters")
    return errors


def validate_form(rules: List[FieldRule], data: Dict[str, str]) -> Dict[str, List[str]]:
    """Validate *data* against *rules*, returning a field -> errors mapping."""
    failures: Dict[str, List[str]] = {}
    for rule in rules:
        errors = validate_rule(rule, data.get(rule.name))
        if errors:
            failures[rule.name] = errors
    return failures


def is_alpha(value: str) -> bool:
    """Return True when *value* contains only letters."""
    return bool(value) and all(ch.isalpha() for ch in value)


def is_alphanumeric(value: str) -> bool:
    """Return True when *value* contains only letters and digits."""
    return bool(value) and all(ch.isalnum() for ch in value)


def validate_url(value: str) -> bool:
    """Return True when *value* is an http(s) URL."""
    return value.startswith(("http://", "https://"))


if __name__ == "__main__":
    print(validate_email("alice@example.com"))