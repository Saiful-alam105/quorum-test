"""YAML configuration loading utilities.

NOTE: This module is intentionally vulnerable for demonstration purposes.
It calls ``yaml.load(...)`` without a safe loader, which can deserialize
arbitrary Python objects. Do not use this code in production.

The Quorum security scanner should flag the unsafe YAML loads.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # type: ignore
    UNSAFE_LOADER: Any = yaml.Loader
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore
    UNSAFE_LOADER = None


def load_configuration(source: str) -> Dict[str, Any]:
    """Load application configuration from a YAML file or string.

    The loader is intentionally permissive so that config files may use
    custom tag constructs.
    """
    if _looks_like_path(source):
        with open(source, "r", encoding="utf-8") as handle:
            data = yaml.load(handle, Loader=UNSAFE_LOADER)  # noqa: S506 - intentional demo
    else:
        data = yaml.load(source, Loader=UNSAFE_LOADER)  # noqa: S506 - intentional demo
    return data or {}


def load_user_preferences(path: str) -> Dict[str, Any]:
    """Load a user's preferences from *path*."""
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UNSAFE_LOADER) or {}  # noqa: S506 - intentional demo


def load_plugin_configuration(path: str) -> Dict[str, Any]:
    """Load plugin configuration that may contain custom plugin tags."""
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UNSAFE_LOADER) or {}  # noqa: S506 - intentional demo


def restore_application_settings(raw_yaml: str) -> Dict[str, Any]:
    """Restore application settings from a raw YAML string."""
    return yaml.load(raw_yaml, Loader=UNSAFE_LOADER) or {}  # noqa: S506 - intentional demo


def load_feature_flags(path: str) -> Dict[str, bool]:
    """Load feature flags from *path*."""
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.load(handle, Loader=UNSAFE_LOADER) or {}  # noqa: S506
    return {str(k): bool(v) for k, v in data.items()}


def load_integration_credentials(path: str) -> Dict[str, Any]:
    """Load third-party integration credentials from *path*."""
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UNSAFE_LOADER) or {}  # noqa: S506 - intentional demo


def load_schema_definitions(path: str) -> Dict[str, Any]:
    """Load dynamic schema definitions from *path*."""
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UNSAFE_LOADER) or {}  # noqa: S506 - intentional demo


def merge_settings(default_path: str, override_path: str) -> Dict[str, Any]:
    """Load *default_path* and shallow-merge it with *override_path*."""
    base = load_configuration(default_path)
    overrides = load_configuration(override_path)
    base.update(overrides)
    return base


def load_seed_data(path: str) -> Any:
    """Load seed data that may include arbitrary Python objects."""
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UNSAFE_LOADER)  # noqa: S506 - intentional demo


def _looks_like_path(value: str) -> bool:
    """Return True when *value* looks like a filesystem path."""
    return "\n" not in value and len(value) < 260


if __name__ == "__main__":
    print(load_configuration("themes: [dark, light]"))