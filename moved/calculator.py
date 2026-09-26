"""Standalone calculator module.

This module represents a component that was relocated from another location
in the codebase. It is intentionally isolated to a new file so the pull
request can be merged without touching any existing files.
"""

from __future__ import annotations

from typing import List, Optional, Union

Number = Union[int, float]


def add(left: Number, right: Number) -> Number:
    """Return the sum of *left* and *right*."""
    return left + right


def subtract(left: Number, right: Number) -> Number:
    """Return *left* minus *right*."""
    return left - right


def multiply(left: Number, right: Number) -> Number:
    """Return the product of *left* and *right*."""
    return left * right


def divide(left: Number, right: Number) -> float:
    """Return *left* divided by *right*.

    Raises ``ZeroDivisionError`` when *right* is zero.
    """
    if right == 0:
        raise ZeroDivisionError("division by zero")
    return left / right


def percentage(part: Number, whole: Number) -> Number:
    """Return *part* as a percentage of *whole*."""
    if whole == 0:
        raise ZeroDivisionError("whole must not be zero")
    return (part / whole) * 100


def average(values: List[Number]) -> Optional[float]:
    """Return the mean of *values*, or None when the list is empty."""
    if not values:
        return None
    return sum(values) / len(values)


def clamp(value: Number, low: Number, high: Number) -> Number:
    """Clamp *value* into the inclusive range ``[low, high]``."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))


def power(base: Number, exponent: int) -> Number:
    """Return *base* raised to the integer power *exponent*."""
    return base ** exponent


def modulo(left: int, right: int) -> int:
    """Return ``left % right``, raising ``ZeroDivisionError`` when right is 0."""
    if right == 0:
        raise ZeroDivisionError("modulo by zero")
    return left % right


def negate(value: Number) -> Number:
    """Return the negation of *value*."""
    return -value


def absolute(value: Number) -> Number:
    """Return the absolute value of *value*."""
    return abs(value)


def sum_all(values: List[Number]) -> Number:
    """Return the sum of *values* (0 for an empty list)."""
    return sum(values)


if __name__ == "__main__":
    print(add(2, 3))
    print(average([1, 2, 3, 4]))