"""Tests for runtime DNS profile resolution."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import cast
from unittest.mock import patch

from dns_zone_bootstrapper.templates.profile_model import FixedDnsProfile
from dns_zone_bootstrapper.templates.profile_resolver import (
    resolve_active_fixed_dns_profile,
)
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)

def test_resolve_active_fixed_dns_profile_falls_back_to_public_safe(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Use the versioned public-safe profile when no local override exists."""
    monkeypatch.chdir(tmp_path)

    missing_local_module = ModuleNotFoundError("No module named 'local'")
    missing_local_module.name = "local"

    with patch(
        "dns_zone_bootstrapper.templates.profile_resolver.importlib.import_module",
        side_effect=missing_local_module,
    ) as mock_import_module:
        resolved_profile = resolve_active_fixed_dns_profile()

    assert resolved_profile is PUBLIC_SAFE_FIXED_DNS_PROFILE
    mock_import_module.assert_called_once_with("local.dns_zone_profile")

def test_resolve_active_fixed_dns_profile_loads_local_override_from_current_working_tree(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Load the gitignored local profile from the current working tree."""
    local_module_path = tmp_path / "local" / "dns_zone_profile.py"
    local_module_path.parent.mkdir()
    local_module_path.write_text(
        "from copy import copy\n"
        "from dns_zone_bootstrapper.templates.profiles.public_safe_candidate "
        "import PUBLIC_SAFE_FIXED_DNS_PROFILE\n"
        "ACTIVE_FIXED_DNS_PROFILE = copy(PUBLIC_SAFE_FIXED_DNS_PROFILE)\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    missing_local_module = ModuleNotFoundError("No module named 'local'")
    missing_local_module.name = "local"

    with patch(
        "dns_zone_bootstrapper.templates.profile_resolver.importlib.import_module",
        side_effect=missing_local_module,
    ) as mock_import_module:
        resolved_profile = resolve_active_fixed_dns_profile()

    assert resolved_profile is not PUBLIC_SAFE_FIXED_DNS_PROFILE
    mock_import_module.assert_called_once_with("local.dns_zone_profile")


def test_resolve_active_fixed_dns_profile_uses_local_override() -> None:
    """Use the gitignored local profile when the override module exists."""
    expected_profile = cast(FixedDnsProfile, object())
    fake_module = SimpleNamespace(ACTIVE_FIXED_DNS_PROFILE=expected_profile)

    with patch(
        "dns_zone_bootstrapper.templates.profile_resolver.importlib.import_module",
        return_value=fake_module,
    ) as mock_import_module:
        resolved_profile = resolve_active_fixed_dns_profile()

    assert resolved_profile is expected_profile
    mock_import_module.assert_called_once_with("local.dns_zone_profile")
