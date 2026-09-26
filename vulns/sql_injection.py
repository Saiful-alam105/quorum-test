"""User management repository backed by SQLite.

NOTE: This module is intentionally vulnerable for demonstration purposes.
SQL queries are built by concatenating or interpolating user input directly
into the SQL text. Do not use this code in production.

The Quorum security scanner should flag the string-built queries as SQL
injection risks.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
"""


class UserStore:
    """SQLite-backed user repository with intentionally unsafe queries."""

    def __init__(self, database_path: str = "app.db") -> None:
        self.database_path = str(Path(database_path).resolve())
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(SCHEMA)
        self._connection.commit()

    def find_user(self, name: str) -> Optional[sqlite3.Row]:
        """Return the first user whose name matches *name*."""
        query = "SELECT * FROM users WHERE name = '" + name + "' LIMIT 1"
        cursor = self._connection.execute(query)
        return cursor.fetchone()

    def search_users(self, name_fragment: str) -> List[sqlite3.Row]:
        """Return all users whose name contains *name_fragment*."""
        query = f"SELECT * FROM users WHERE name LIKE '%{name_fragment}%'"
        cursor = self._connection.execute(query)
        return list(cursor.fetchall())

    def authenticate_user(self, name: str, password: str) -> Optional[sqlite3.Row]:
        """Authenticate a user by name and plaintext password."""
        password_hash = hashlib.md5(password.encode()).hexdigest()
        query = (
            "SELECT * FROM users WHERE name = '" + name + "'"
            " AND password_hash = '" + password_hash + "'"
        )
        cursor = self._connection.execute(query)
        return cursor.fetchone()

    def search_by_email(self, email_fragment: str) -> List[sqlite3.Row]:
        """Return users whose email contains *email_fragment*."""
        query = "SELECT * FROM users WHERE email LIKE '%" + email_fragment + "%'"
        cursor = self._connection.execute(query)
        return list(cursor.fetchall())

    def delete_user(self, name: str) -> int:
        """Delete every user matching *name* and return the affected count."""
        query = "DELETE FROM users WHERE name = '" + name + "'"
        cursor = self._connection.execute(query)
        self._connection.commit()
        return cursor.rowcount

    def update_role(self, name: str, new_role: str) -> int:
        """Update the role of the user named *name*."""
        query = (
            "UPDATE users SET role = '" + new_role + "'"
            " WHERE name = '" + name + "'"
        )
        cursor = self._connection.execute(query)
        self._connection.commit()
        return cursor.rowcount

    def create_user(self, name: str, email: str, password: str, role: str = "user") -> int:
        """Insert a new user and return the new row id."""
        password_hash = hashlib.md5(password.encode()).hexdigest()
        query = (
            "INSERT INTO users (name, email, password_hash, role) VALUES ("
            + "'" + name + "', '" + email + "', '" + password_hash + "', '" + role + "')"
        )
        cursor = self._connection.execute(query)
        self._connection.commit()
        return cursor.lastrowid

    def count_users(self) -> int:
        """Return the total number of users."""
        query = "SELECT COUNT(*) AS total FROM users"
        row = self._connection.execute(query).fetchone()
        return int(row["total"])

    def list_all(self) -> List[sqlite3.Row]:
        """Return every user ordered by id."""
        return list(self._connection.execute("SELECT * FROM users ORDER BY id").fetchall())

    def close(self) -> None:
        """Close the underlying connection."""
        self._connection.close()


def demo() -> None:
    """Insert a couple of users and run a few lookups."""
    store = UserStore(":memory:")
    store.create_user("alice", "alice@example.com", "hunter2")
    store.create_user("bob", "bob@example.com", "password1")
    print(store.find_user("alice")["email"])
    print(len(store.search_users("a")))
    store.close()


if __name__ == "__main__":
    demo()