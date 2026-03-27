"""Bootstrap tests."""

from typer.testing import CliRunner

from dns_zone_bootstrapper import __version__
from dns_zone_bootstrapper.interfaces.cli.app import app as cli_app
from dns_zone_bootstrapper.interfaces.web.app import app as web_app
from dns_zone_bootstrapper.interfaces.web.app import health
from dns_zone_bootstrapper.interfaces.web.app import root

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


def test_web_root_returns_html_response_with_minimal_c0_content() -> None:
    """Root route exposes the minimal HTML page for C0."""
    response = root()
    html = response.body.decode("utf-8")

    assert response.status_code == 200
    assert response.media_type == "text/html"
    assert "DNS Zone Bootstrapper" in html
    assert "Dominio apex" in html
    assert "Genera e scarica il file (.txt)" in html
    assert "C0" in html
    assert "C1" in html


def test_web_health_returns_ok_status_payload() -> None:
    """Health route preserves the minimal bootstrap health contract."""
    assert health() == {"status": "ok"}


def test_web_app_exposes_root_and_health_routes() -> None:
    """Web app exposes the minimal expected public routes."""
    routes = {
        route.path: sorted(route.methods)
        for route in web_app.routes
    }

    assert routes["/"] == ["GET"]
    assert routes["/health"] == ["GET"]
