"""Pure-Python math helpers for pricing and statistics.

This PR is intended to demonstrate Quorum's Python analysis and test
generation. No tests are included here so that Quorum can generate them.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Union

Number = Union[int, float]


def calculate_discount(price: Number, discount_percent: Number) -> Number:
    """Return *price* reduced by *discount_percent*.

    Raises ``ValueError`` when *discount_percent* is outside 0..100.
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount must be between 0 and 100")
    return price - (price * discount_percent / 100)


def apply_tax(amount: Number, tax_percent: Number) -> Number:
    """Return *amount* plus *tax_percent* tax.

    Raises ``ValueError`` for negative tax rates.
    """
    if tax_percent < 0:
        raise ValueError("tax rate must not be negative")
    return amount + (amount * tax_percent / 100)


def calculate_total(price: Number, quantity: int) -> Number:
    """Return the total for *quantity* items at *price* each."""
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    return price * quantity


def calculate_average(values: Iterable[Number]) -> Optional[float]:
    """Return the arithmetic mean of *values*, or None when empty."""
    items = list(values)
    if not items:
        return None
    return sum(items) / len(items)


def clamp_value(value: Number, low: Number, high: Number) -> Number:
    """Clamp *value* into the inclusive range ``[low, high]``."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))


def calculate_percentage(part: Number, whole: Number) -> Number:
    """Return *part* as a percentage of *whole*."""
    if whole == 0:
        raise ZeroDivisionError("whole must not be zero")
    return (part / whole) * 100


def calculate_compound_value(
    principal: Number, rate_percent: Number, periods: int
) -> Number:
    """Return the future value of *principal* compounding at *rate_percent*."""
    if principal < 0:
        raise ValueError("principal must not be negative")
    if periods < 0:
        raise ValueError("periods must not be negative")
    rate = rate_percent / 100
    return principal * ((1 + rate) ** periods)


def calculate_installment(
    principal: Number, annual_rate_percent: Number, months: int
) -> Number:
    """Return the fixed monthly payment for a simple-interest loan.

    Uses the standard amortization formula. Returns ``principal / months``
    when the annual rate is zero.
    """
    if principal <= 0:
        raise ValueError("principal must be positive")
    if months <= 0:
        raise ValueError("months must be positive")
    if annual_rate_percent == 0:
        return principal / months
    monthly_rate = annual_rate_percent / 100 / 12
    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)


def total_with_discount_and_tax(
    price: Number,
    quantity: int,
    discount_percent: Number = 0,
    tax_percent: Number = 0,
) -> Number:
    """Return the final amount after applying quantity, discount and tax."""
    subtotal = calculate_total(price, quantity)
    after_discount = calculate_discount(subtotal, discount_percent)
    return apply_tax(after_discount, tax_percent)


def round_money(amount: Number) -> Number:
    """Round *amount* to two decimal places."""
    return round(amount, 2)


def percentile(values: List[Number], percent: Number) -> Number:
    """Return the *percent*-th percentile of *values* (nearest-rank method)."""
    if not values:
        raise ValueError("values must not be empty")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    ordered = sorted(values)
    rank = max(1, min(len(ordered), int((percent / 100) * len(ordered)) + 1))
    return ordered[rank - 1]


def running_average(values: Iterable[Number]) -> List[float]:
    """Return the cumulative running average at each position."""
    items = list(values)
    result: List[float] = []
    total = 0.0
    for index, value in enumerate(items, start=1):
        total += value
        result.append(total / index)
    return result


if __name__ == "__main__":
    print(total_with_discount_and_tax(100, 2, 10, 5))