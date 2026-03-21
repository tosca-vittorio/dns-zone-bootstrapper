"""Application use case for zone apex validation."""

from __future__ import annotations

from dataclasses import dataclass

from dns_zone_bootstrapper.domain.domain_validation import (
    is_valid_zone_apex_candidate,
)


@dataclass(frozen=True, slots=True)
class ZoneApexValidationResult:
    """Structured result returned by the zone apex validation use case."""

    input_value: str
    is_valid: bool
    zone_apex: str | None
    error_code: str | None


def validate_zone_apex_input(input_value: str) -> ZoneApexValidationResult:
    """Validate a zone apex input and return a minimal structured result."""
    is_valid = is_valid_zone_apex_candidate(input_value)
    zone_apex = input_value if is_valid else None
    error_code = None if is_valid else "invalid_zone_apex_candidate"

    return ZoneApexValidationResult(
        input_value=input_value,
        is_valid=is_valid,
        zone_apex=zone_apex,
        error_code=error_code,
    )
