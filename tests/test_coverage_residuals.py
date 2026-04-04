"""Residual coverage tests for low-risk package branches."""

from __future__ import annotations

from pathlib import Path
import sys
import runpy
from unittest.mock import patch

import pytest

from dns_zone_bootstrapper.interfaces.web.app import _error_message_from_code
from dns_zone_bootstrapper.templates.profile_resolver import (
    _load_local_profile_module_from_current_working_tree,
    resolve_active_fixed_dns_profile,
)


def test_cli_app_module_runs_main_entrypoint_when_executed_as_script() -> None:
    """Executing the CLI module as __main__ should invoke the Typer app."""
    module_name = "dns_zone_bootstrapper.interfaces.cli.app"
    original_module = sys.modules.pop(module_name, None)

    try:
        with patch("typer.main.Typer.__call__", return_value=None) as mock_call:
            runpy.run_module(
                module_name,
                run_name="__main__",
            )
    finally:
        if original_module is not None:
            sys.modules[module_name] = original_module

    mock_call.assert_called_once_with()


def test_error_message_from_code_returns_generic_message_for_none() -> None:
    """None error code should map to the generic invalid request message."""
    assert _error_message_from_code(None) == "Richiesta non valida."


def test_load_local_profile_module_from_current_working_tree_returns_none_when_spec_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Missing import spec should gracefully return None."""
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    (local_dir / "dns_zone_profile.py").write_text(
        "ACTIVE_FIXED_DNS_PROFILE = None\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    with patch(
        "dns_zone_bootstrapper.templates.profile_resolver."
        "importlib.util.spec_from_file_location",
        return_value=None,
    ):
        assert _load_local_profile_module_from_current_working_tree() is None


def test_resolve_active_fixed_dns_profile_reraises_unexpected_module_not_found() -> None:
    """Unexpected ModuleNotFoundError should not be swallowed by the resolver."""
    error = ModuleNotFoundError("unexpected import failure")
    error.name = "unexpected.module"

    with patch(
        "dns_zone_bootstrapper.templates.profile_resolver.importlib.import_module",
        side_effect=error,
    ):
        with pytest.raises(ModuleNotFoundError, match="unexpected import failure"):
            resolve_active_fixed_dns_profile()
