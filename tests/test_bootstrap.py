"""Bootstrap tests."""

from typer.testing import CliRunner

from dns_zone_bootstrapper import __version__
from dns_zone_bootstrapper.interfaces.cli.app import app as cli_app
from dns_zone_bootstrapper.interfaces.web.app import app as web_app

runner = CliRunner()


def test_package_version() -> None:
    """Package exposes a version."""
    assert __version__ == "0.1.0"


def test_cli_has_help() -> None:
    """CLI app is configured."""
    assert cli_app.info.help == "CLI for DNS Zone Bootstrapper."


def test_cli_doctor_command() -> None:
    """CLI doctor subcommand works."""
    result = runner.invoke(cli_app, ["doctor"])
    assert result.exit_code == 0
    assert "dns-zone-bootstrapper: CLI bootstrap OK" in result.stdout


def test_web_metadata() -> None:
    """Web app metadata is present."""
    assert web_app.title == "DNS Zone Bootstrapper"
