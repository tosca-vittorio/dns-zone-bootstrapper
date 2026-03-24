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

def test_validate_zone_apex_input_propagates_specific_failure_reason() -> None:
    """Return a structured failure result with a specific error code."""
    result = validate_zone_apex_input(" example.com ")

    assert result == ZoneApexValidationResult(
        input_value=" example.com ",
        is_valid=False,
        zone_apex=None,
        error_code="surrounding_whitespace",
    )

def test_validate_zone_apex_input_propagates_non_string_input_failure() -> None:
    """Return a structured failure result for non-string zone apex input."""
    result = validate_zone_apex_input(None)

    assert result == ZoneApexValidationResult(
        input_value=None,
        is_valid=False,
        zone_apex=None,
        error_code="non_string_input",
    )
