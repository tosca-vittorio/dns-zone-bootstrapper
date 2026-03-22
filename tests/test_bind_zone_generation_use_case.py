"""Tests for the bind zone generation application use case."""

from pathlib import Path

from tests.shared_bind_zone_assertions import (
    assert_alpha_zone_derived_rendering,
)

from dns_zone_bootstrapper.application.bind_zone_generation import (
    BindZoneFileGenerationResult,
    generate_bind_zone_file,
)


def test_generate_bind_zone_file_returns_structured_success_with_rendered_text() -> None:
    """Return a structured success result with the rendered BIND text."""
    result = generate_bind_zone_file("testdomain.com")

    golden_path = Path(__file__).parent / "golden" / "public_safe_candidate.bind.txt"
    expected_text = golden_path.read_text(encoding="utf-8")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com",
        is_valid=True,
        zone_apex="testdomain.com",
        error_code=None,
        zone_file_text=expected_text,
    )


def test_generate_bind_zone_file_propagates_validation_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for invalid input."""
    result = generate_bind_zone_file(" testdomain.com ")

    assert result == BindZoneFileGenerationResult(
        input_value=" testdomain.com ",
        is_valid=False,
        zone_apex=None,
        error_code="surrounding_whitespace",
        zone_file_text=None,
    )

def test_generate_bind_zone_file_renders_non_golden_valid_apex_end_to_end() -> None:
    """Render a valid non-golden apex end-to-end through the application use case."""
    result = generate_bind_zone_file("alpha-zone.example.org")

    assert result.input_value == "alpha-zone.example.org"
    assert result.is_valid is True
    assert result.zone_apex == "alpha-zone.example.org"
    assert result.error_code is None
    assert result.zone_file_text is not None

    assert_alpha_zone_derived_rendering(result.zone_file_text)
