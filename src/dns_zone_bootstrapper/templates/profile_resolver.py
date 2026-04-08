"""Runtime boundary for fixed DNS profile resolution."""

from __future__ import annotations

import importlib
import importlib.util
import os
from pathlib import Path
from types import ModuleType
from typing import cast

from dns_zone_bootstrapper.templates.profile_model import FixedDnsProfile
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)

_EXPLICIT_PROFILE_PATH_ENV = "DNS_ZONE_PROFILE_PATH"
_LOCAL_PROFILE_MODULE = "local.dns_zone_profile"
_LOCAL_PROFILE_PATH = Path("local/dns_zone_profile.py")


def _load_profile_module_from_path(
    module_name: str,
    profile_path: Path,
) -> ModuleType | None:
    """Load a Python module from an explicit file path."""
    if not profile_path.is_file():
        return None

    spec = importlib.util.spec_from_file_location(module_name, profile_path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _read_active_profile(module: ModuleType, source_label: str) -> FixedDnsProfile:
    """Extract the active fixed DNS profile from a loaded module."""
    try:
        return cast(FixedDnsProfile, module.ACTIVE_FIXED_DNS_PROFILE)
    except AttributeError as error:
        raise RuntimeError(
            f"Missing ACTIVE_FIXED_DNS_PROFILE in {source_label}."
        ) from error


def _load_profile_module_from_explicit_env_path() -> ModuleType | None:
    """Load the fixed DNS profile module from an explicit runtime path."""
    raw_path = os.environ.get(_EXPLICIT_PROFILE_PATH_ENV, "").strip()
    if not raw_path:
        return None

    profile_path = Path(raw_path)
    module = _load_profile_module_from_path(
        module_name="runtime.explicit_dns_zone_profile",
        profile_path=profile_path,
    )
    if module is None:
        raise RuntimeError(
            "Configured DNS_ZONE_PROFILE_PATH is missing or unreadable: "
            f"{profile_path}"
        )

    return module


def _load_local_profile_module_from_current_working_tree() -> ModuleType | None:
    """Load the gitignored local profile module from the current working tree."""
    return _load_profile_module_from_path(
        module_name=_LOCAL_PROFILE_MODULE,
        profile_path=Path.cwd() / _LOCAL_PROFILE_PATH,
    )


def resolve_active_fixed_dns_profile() -> FixedDnsProfile:
    """Return the active fixed DNS profile for runtime generation.

    Resolution order:
    1. explicit runtime path from DNS_ZONE_PROFILE_PATH
    2. importable local.dns_zone_profile
    3. ./local/dns_zone_profile.py in current working tree
    4. versioned public-safe profile fallback
    """
    explicit_module = _load_profile_module_from_explicit_env_path()
    if explicit_module is not None:
        return _read_active_profile(
            explicit_module,
            source_label=_EXPLICIT_PROFILE_PATH_ENV,
        )

    try:
        module = importlib.import_module(_LOCAL_PROFILE_MODULE)
    except ModuleNotFoundError as error:
        if error.name not in {"local", _LOCAL_PROFILE_MODULE}:
            raise

        module = _load_local_profile_module_from_current_working_tree()
        if module is None:
            return PUBLIC_SAFE_FIXED_DNS_PROFILE

    return _read_active_profile(module, source_label=_LOCAL_PROFILE_MODULE)
