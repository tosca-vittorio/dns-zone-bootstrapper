"""Tests for the zone apex validation use case."""

from dns_zone_bootstrapper.application.zone_apex_validation import (
    ZoneApexValidationResult,
    validate_zone_apex_input,
)


def test_validate_zone_apex_input_returns_structured_success() -> None:
    """Return a structured success result for a valid zone apex input."""
    result = validate_zone_apex_input("example.com")

    assert result == ZoneApexValidationResult(
        input_value="example.com",
        is_valid=True,
        zone_apex="example.com",
        error_code=None,
    )


def test_validate_zone_apex_input_returns_structured_failure() -> None:
    """Return a structured failure result for an invalid zone apex input."""
    result = validate_zone_apex_input(" example.com ")

    assert result == ZoneApexValidationResult(
        input_value=" example.com ",
        is_valid=False,
        zone_apex=None,
        error_code="invalid_zone_apex_candidate",
    )
