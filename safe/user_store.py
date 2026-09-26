"""SQLite-backed user repository using only parameterized queries.

This module intentionally demonstrates a *safer* implementation for
comparison with the vulnerable SQL demo. Every query uses ``?`` placeholders
so user input can never alter the query structure (no SQL injection).
"""

from __future__ import annotations

import hashlib
import hmac
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class User:
    """A user row returned from the store."""

    id: int
    name: str
    email: str
    role: str


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
"""


class UserStore:
    """A parameterized SQLite repository for users."""

    def __init__(self, database_path: str = "app.db") -> None:
        self.database_path = str(Path(database_path).resolve())
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(SCHEMA)
        self._connection.commit()

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        """Hash *password* with *salt* using a simple keyed digest."""
        return hmac.new(salt, password.encode("utf-8"), hashlib.sha256).hexdigest()

    def create_user(self, name: str, email: str, password: str, role: str = "user") -> int:
        """Insert a new user and return its id."""
        salt = __import__("os").urandom(16)
        password_hash = self._hash_password(password, salt)
        cursor = self._connection.execute(
            "INSERT INTO users (name, email, password_hash, role)"
            " VALUES (?, ?, ?, ?)",
            (name, email, f"{salt.hex()}:{password_hash}", role),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def find_user(self, name: str) -> Optional[User]:
        """Return the user named *name* or None."""
        row = self._connection.execute(
            "SELECT * FROM users WHERE name = ?", (name,)
        ).fetchone()
        return self._to_user(row)

    def find_user_by_id(self, user_id: int) -> Optional[User]:
        """Return the user with the given id or None."""
        row = self._connection.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return self._to_user(row)

    def search_users(self, name_fragment: str) -> List[User]:
        """Return users whose name contains *name_fragment*."""
        rows = self._connection.execute(
            "SELECT * FROM users WHERE name LIKE ? ORDER BY name",
            (f"%{name_fragment}%",),
        ).fetchall()
        return [self._to_user(row) for row in rows if row is not None]

    def update_user(self, user_id: int, email: Optional[str] = None,
                    role: Optional[str] = None) -> bool:
        """Update *email* and/or *role* for *user_id*."""
        if email is not None:
            self._connection.execute(
                "UPDATE users SET email = ? WHERE id = ?", (email, user_id)
            )
        if role is not None:
            self._connection.execute(
                "UPDATE users SET role = ? WHERE id = ?", (role, user_id)
            )
        self._connection.commit()
        return True

    def delete_user(self, user_id: int) -> bool:
        """Delete the user with *user_id*."""
        cursor = self._connection.execute(
            "DELETE FROM users WHERE id = ?", (user_id,)
        )
        self._connection.commit()
        return cursor.rowcount > 0

    def authenticate_user(self, name: str, password: str) -> Optional[User]:
        """Authenticate *name* with *password*, returning the user or None."""
        row = self._connection.execute(
            "SELECT * FROM users WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            return None
        salt, stored_hash = row["password_hash"].split(":", 1)
        candidate = self._hash_password(password, bytes.fromhex(salt))
        if not hmac.compare_digest(candidate, stored_hash):
            return None
        return self._to_user(row)

    def count_users(self) -> int:
        """Return the total number of users."""
        row = self._connection.execute("SELECT COUNT(*) AS total FROM users").fetchone()
        return int(row["total"])

    def list_all(self) -> List[User]:
        """Return every user ordered by name."""
        rows = self._connection.execute("SELECT * FROM users ORDER BY name").fetchall()
        return [self._to_user(row) for row in rows if row is not None]

    def close(self) -> None:
        """Close the underlying connection."""
        self._connection.close()

    @staticmethod
    def _to_user(row: Optional[sqlite3.Row]) -> Optional[User]:
        if row is None:
            return None
        return User(id=int(row["id"]), name=row["name"], email=row["email"], role=row["role"])


def demo() -> None:
    """Insert sample users and run a few parameterized lookups."""
    store = UserStore(":memory:")
    store.create_user("alice", "alice@example.com", "correct-horse")
    store.create_user("bob", "bob@example.com", "battery-staple")
    print(store.authenticate_user("alice", "correct-horse"))
    print(len(store.search_users("a")))
    store.close()


if __name__ == "__main__":
    demo()