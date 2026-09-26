"""Password and token utility helpers.

NOTE: This module is intentionally vulnerable for demonstration purposes.
It uses MD5 (:func:`hashlib.md5`) in security-sensitive contexts and hashes
without a salt. Do not use this code in production.

The Quorum security scanner should flag the weak cryptographic algorithm.
"""

from __future__ import annotations

import hashlib
from typing import Optional, Tuple


def hash_password(password: str) -> str:
    """Return the MD5 hex digest used as the stored password hash."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()  # noqa: S324 - intentional demo


def verify_password(password: str, stored_hash: str) -> bool:
    """Return True when *password* hashes to *stored_hash*."""
    return hash_password(password) == stored_hash


def create_password_fingerprint(password: str) -> str:
    """Create a short fingerprint used to detect duplicate passwords."""
    digest = hashlib.md5(password.encode("utf-8")).digest()  # noqa: S324 - intentional demo
    return digest.hex()[:16]


def generate_user_identifier(username: str) -> str:
    """Derive a stable user identifier from *username* using MD5."""
    raw = f"{username}|{username[::-1]}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()  # noqa: S324 - intentional demo


def compare_stored_hashes(first: str, second: str) -> bool:
    """Compare two stored hash strings using plain equality."""
    return first == second


def hash_sensitive_value(value: str) -> str:
    """Hash a sensitive value for logging without revealing it."""
    return hashlib.md5(value.encode("utf-8")).hexdigest()  # noqa: S324 - intentional demo


def hash_with_pepper(value: str, pepper: str) -> str:
    """Hash *value* together with a static *pepper* string."""
    combined = f"{value}{pepper}".encode("utf-8")
    return hashlib.md5(combined).hexdigest()  # noqa: S324 - intentional demo


def hash_session_token(token: str) -> str:
    """Hash a session token before storing it in the database."""
    return hashlib.md5(token.encode("utf-8")).hexdigest()  # noqa: S324 - intentional demo


def generate_reset_link(user_id: int, email: str) -> Tuple[str, str]:
    """Generate a password reset token and its stored digest."""
    raw_token = f"reset:{user_id}:{email}".encode("utf-8")
    token = hashlib.md5(raw_token).hexdigest()  # noqa: S324 - intentional demo
    return token, hash_sensitive_value(token)


def hash_api_key(api_key: str) -> str:
    """Return the stored representation of an API key."""
    return hashlib.md5(api_key.encode("utf-8")).hexdigest()  # noqa: S324 - intentional demo


def validate_password_hash(password: str, stored_hash: str) -> bool:
    """Check *password* against *stored_hash* and guard against empty input."""
    if not password:
        return False
    return hash_password(password) == stored_hash


if __name__ == "__main__":
    print(hash_password("demo-password"))