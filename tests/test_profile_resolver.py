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

def test_resolve_active_fixed_dns_profile_uses_explicit_env_path(
    monkeypatch,
    tmp_path,
):
    """Use the explicit environment path when configured."""
    profile_file = tmp_path / "explicit_dns_zone_profile.py"
    profile_file.write_text(
        """
from dns_zone_bootstrapper.templates.profile_model import (
    DnsRecordTemplate,
    FixedDnsProfile,
    RdataTemplateSpec,
)

ACTIVE_FIXED_DNS_PROFILE = FixedDnsProfile(
    profile_name="explicit_env_profile",
    records=(
        DnsRecordTemplate(
            record_type="A",
            owner_template="@",
            ttl=1,
            record_class="IN",
            rdata=RdataTemplateSpec(
                kind="fixed",
                template="203.0.113.10",
            ),
            cf_proxied=True,
        ),
    ),
)
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setenv("DNS_ZONE_PROFILE_PATH", str(profile_file))

    profile = resolve_active_fixed_dns_profile()

    assert profile.profile_name == "explicit_env_profile"
    assert len(profile.records) == 1
    assert profile.records[0].rdata.template == "203.0.113.10"

def test_resolve_active_fixed_dns_profile_fails_for_missing_explicit_profile_file(
    monkeypatch,
    tmp_path,
):
    """Fail when the explicit environment path points to a missing file."""
    missing_profile = tmp_path / "missing_dns_zone_profile.py"
    monkeypatch.setenv("DNS_ZONE_PROFILE_PATH", str(missing_profile))

    try:
        resolve_active_fixed_dns_profile()
    except RuntimeError as error:
        assert "Configured DNS_ZONE_PROFILE_PATH is missing or unreadable" in str(error)
    else:
        raise AssertionError("Expected RuntimeError for missing explicit profile path.")


def test_resolve_active_fixed_dns_profile_fails_when_explicit_module_has_no_active_profile(
    monkeypatch,
    tmp_path,
):
    """Fail when the explicit environment module lacks ACTIVE_FIXED_DNS_PROFILE."""
    profile_file = tmp_path / "broken_dns_zone_profile.py"
    profile_file.write_text(
        """
BROKEN = True
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setenv("DNS_ZONE_PROFILE_PATH", str(profile_file))

    try:
        resolve_active_fixed_dns_profile()
    except RuntimeError as error:
        assert "Missing ACTIVE_FIXED_DNS_PROFILE in DNS_ZONE_PROFILE_PATH." == str(error)
    else:
        raise AssertionError("Expected RuntimeError for missing ACTIVE_FIXED_DNS_PROFILE.")
