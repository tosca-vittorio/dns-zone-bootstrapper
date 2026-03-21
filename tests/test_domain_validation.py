"""Tests for domain apex candidate validation."""

import pytest

from dns_zone_bootstrapper.domain.domain_validation import (
    ZoneApexCandidateValidationResult,
    is_valid_zone_apex_candidate,
    validate_zone_apex_candidate,
)


@pytest.mark.parametrize(
    ("domain", "expected"),
    [
        ("example.com", True),
        ("example.co.uk", True),
        ("", False),
        (" example.com ", False),
        ("localhost", False),
        ("example.com.", False),
        ("example..com", False),
        ("-example.com", False),
        ("example-.com", False),
        ("exa_mple.com", False),
    ],
)
def test_zone_apex_candidate_validation(domain: str, expected: bool) -> None:
    """Validate accepted and rejected domain apex candidate inputs."""
    assert is_valid_zone_apex_candidate(domain) is expected


@pytest.mark.parametrize(
    ("domain", "error_code"),
    [
        ("", "empty_input"),
        (" example.com ", "surrounding_whitespace"),
        ("localhost", "missing_dot"),
        (".example.com", "leading_dot"),
        ("example.com.", "trailing_dot"),
        ("example..com", "empty_label"),
        ("exa_mple.com", "invalid_label"),
    ],
)
def test_validate_zone_apex_candidate_returns_specific_error_codes(
    domain: str,
    error_code: str,
) -> None:
    """Return deterministic error codes for invalid zone apex candidates."""
    result = validate_zone_apex_candidate(domain)

    assert result == ZoneApexCandidateValidationResult(
        is_valid=False,
        error_code=error_code,
    )


def test_validate_zone_apex_candidate_returns_success_result() -> None:
    """Return a success result for a valid zone apex candidate."""
    result = validate_zone_apex_candidate("example.com")

    assert result == ZoneApexCandidateValidationResult(
        is_valid=True,
        error_code=None,
    )
