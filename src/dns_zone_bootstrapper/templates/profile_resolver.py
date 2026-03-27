"""Runtime boundary for fixed DNS profile resolution."""

from __future__ import annotations

import importlib
from typing import cast

from dns_zone_bootstrapper.templates.profile_model import FixedDnsProfile
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)

_LOCAL_PROFILE_MODULE = "local.dns_zone_profile"


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
        return PUBLIC_SAFE_FIXED_DNS_PROFILE

    return cast(FixedDnsProfile, module.ACTIVE_FIXED_DNS_PROFILE)
