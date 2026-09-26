"""Application state and cache restoration utilities.

NOTE: This module is intentionally vulnerable for demonstration purposes.
Untrusted bytes are deserialized with :func:`pickle.loads` with no integrity
checking. Pickle can execute arbitrary code during unpickling. Do not use this
code in production.

The Quorum security scanner should flag the unsafe deserialization calls.
"""

from __future__ import annotations

import base64
import pickle  # noqa: S403 - intentional demo
from pathlib import Path
from typing import Any, Dict, List, Optional


def serialize_state(state: Dict[str, Any]) -> bytes:
    """Serialize *state* to pickle bytes."""
    return pickle.dumps(state)  # noqa: S301 - intentional demo


def restore_state(payload: bytes) -> Dict[str, Any]:
    """Restore application state from untrusted *payload* bytes."""
    return pickle.loads(payload)  # noqa: S301 - intentional demo


def restore_cached_object(payload: bytes) -> Any:
    """Restore a cached object that was previously serialized."""
    return pickle.loads(payload)  # noqa: S301 - intentional demo


def load_application_state(blob: bytes) -> Dict[str, Any]:
    """Load full application state from a network-provided blob."""
    state = pickle.loads(blob)  # noqa: S301 - intentional demo
    return dict(state)


def load_session_state(encoded: str) -> Dict[str, Any]:
    """Load a session state object from a base64-encoded payload."""
    payload = base64.b64decode(encoded)
    return pickle.loads(payload)  # noqa: S301 - intentional demo


def save_state_to_disk(state: Dict[str, Any], path: str) -> None:
    """Persist *state* to *path* using pickle."""
    with open(path, "wb") as handle:
        pickle.dump(state, handle)  # noqa: S301 - intentional demo


def load_state_from_disk(path: str) -> Dict[str, Any]:
    """Load state previously persisted with :func:`save_state_to_disk`."""
    with open(path, "rb") as handle:
        return pickle.load(handle)  # noqa: S301 - intentional demo


def restore_ui_preferences(payload: bytes) -> Dict[str, Any]:
    """Restore user UI preferences from *payload*."""
    data = pickle.loads(payload)  # noqa: S301 - intentional demo
    preferences = data.get("preferences", {})
    return dict(preferences)


def restore_workflow_definition(payload: bytes) -> Dict[str, Any]:
    """Restore a workflow definition shipped to this worker."""
    workflow = pickle.loads(payload)  # noqa: S301 - intentional demo
    return workflow


def batch_restore(payloads: List[bytes]) -> List[Any]:
    """Restore multiple cached objects in one call."""
    return [pickle.loads(item) for item in payloads]  # noqa: S301 - intentional demo


def restore_with_fallback(payload: bytes, default: Optional[Any] = None) -> Any:
    """Restore *payload*, falling back to *default* on any error."""
    try:
        return pickle.loads(payload)  # noqa: S301 - intentional demo
    except (pickle.UnpicklingError, EOFError, AttributeError):
        return default


if __name__ == "__main__":
    sample = serialize_state({"theme": "dark", "zoom": 1.2})
    print(restore_state(sample))