"""Runtime boundary for fixed DNS profile resolution."""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import cast

from dns_zone_bootstrapper.templates.profile_model import FixedDnsProfile
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)

_LOCAL_PROFILE_MODULE = "local.dns_zone_profile"
_LOCAL_PROFILE_PATH = Path("local/dns_zone_profile.py")

def _load_local_profile_module_from_current_working_tree() -> ModuleType | None:
    """Load the gitignored local profile module from the current working tree."""
    profile_path = Path.cwd() / _LOCAL_PROFILE_PATH

    if not profile_path.is_file():
        return None

    spec = importlib.util.spec_from_file_location(
        _LOCAL_PROFILE_MODULE,
        profile_path,
    )
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

def resolve_active_fixed_dns_profile() -> FixedDnsProfile:
    """Return the active fixed DNS profile for runtime generation.

    Falls back to the versioned public-safe profile when no local override
    module is available.
    """
    try:
        module = importlib.import_module(_LOCAL_PROFILE_MODULE)
    except ModuleNotFoundError as error:
        if error.name not in {"local", _LOCAL_PROFILE_MODULE}:
            raise

        module = _load_local_profile_module_from_current_working_tree()
        if module is None:
            return PUBLIC_SAFE_FIXED_DNS_PROFILE

    return cast(FixedDnsProfile, module.ACTIVE_FIXED_DNS_PROFILE)
