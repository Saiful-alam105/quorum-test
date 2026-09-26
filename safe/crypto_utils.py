"""Security utility helpers using modern primitives.

This module intentionally demonstrates a *safer* implementation for
comparison with the vulnerable weak-hash demo. It uses :mod:`secrets` for
security-sensitive randomness and salted PBKDF2-HMAC-SHA256 for passwords.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from typing import Optional, Tuple


PASSWORD_ALGORITHM = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16


def generate_token(byte_length: int = 32) -> str:
    """Return a URL-safe random token with *byte_length* bytes of entropy."""
    if byte_length < 16:
        raise ValueError("token entropy must be at least 16 bytes")
    return secrets.token_urlsafe(byte_length)


def generate_api_key() -> str:
    """Return a fresh API key in the ``qk_`` prefix format."""
    return f"qk_{secrets.token_urlsafe(32)}"


def hash_password(password: str) -> str:
    """Hash *password* with a random salt using PBKDF2-HMAC-SHA256.

    Returns a self-describing string: ``pbkdf2_sha256$iterations$salt$hash``.
    """
    if not password:
        raise ValueError("password must not be empty")
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return "$".join(
        [
            PASSWORD_ALGORITHM,
            str(PBKDF2_ITERATIONS),
            base64.urlsafe_b64encode(salt).decode("ascii"),
            base64.urlsafe_b64encode(digest).decode("ascii"),
        ]
    )


def verify_password(password: str, stored: str) -> bool:
    """Verify *password* against a value produced by :func:`hash_password`."""
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored.split("$")
    except ValueError:
        return False
    if algorithm != PASSWORD_ALGORITHM:
        return False
    salt = base64.urlsafe_b64decode(salt_b64)
    expected = base64.urlsafe_b64decode(digest_b64)
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, int(iterations)
    )
    return hmac.compare_digest(candidate, expected)


def constant_time_compare(left: str, right: str) -> bool:
    """Compare two strings in constant time."""
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def create_token_record() -> Tuple[str, str]:
    """Generate a token and a stored hash for persistence.

    Returns ``(token, stored_hash)``. Only *stored_hash* should be saved.
    """
    token = generate_token(32)
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    stored = base64.urlsafe_b64encode(digest).decode("ascii")
    return token, stored


def validate_token(token: str, stored_hash: str) -> bool:
    """Return True when *token* matches the *stored_hash*."""
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    candidate = base64.urlsafe_b64encode(digest).decode("ascii")
    return hmac.compare_digest(candidate, stored_hash)


def generate_reset_token_for(user_id: int) -> Tuple[str, str]:
    """Generate a password reset token bound to *user_id*."""
    raw = f"{user_id}.{secrets.token_hex(16)}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return raw, digest


def random_hex(byte_length: int = 16) -> str:
    """Return *byte_length* random bytes as lowercase hex."""
    return secrets.token_hex(byte_length)


def is_strong_password(password: str, min_length: int = 12) -> bool:
    """Return True when *password* meets basic strength checks."""
    if len(password) < min_length:
        return False
    return (
        any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
    )


def safe_hash(value: str) -> str:
    """Return a salted SHA-256 digest for *value* (non-password use)."""
    salt = secrets.token_bytes(8)
    digest = hashlib.sha256(salt + value.encode("utf-8")).digest()
    return f"{salt.hex()}:{digest.hex()}"


if __name__ == "__main__":
    stored = hash_password("demo-password")
    print(verify_password("demo-password", stored))