"""Tests for domain apex candidate validation."""

import pytest

from dns_zone_bootstrapper.domain.domain_validation import (
    is_valid_zone_apex_candidate,
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
