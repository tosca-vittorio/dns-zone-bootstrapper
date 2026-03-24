"""Application use case for zone apex validation."""

from __future__ import annotations

from dataclasses import dataclass

from dns_zone_bootstrapper.domain.domain_validation import (
    validate_zone_apex_candidate,
)


@dataclass(frozen=True, slots=True)
class ZoneApexValidationResult:
    """Structured result returned by the zone apex validation use case."""

    input_value: object
    is_valid: bool
    zone_apex: str | None
    error_code: str | None


def validate_zone_apex_input(input_value: object) -> ZoneApexValidationResult:
    """Validate a zone apex input and return a minimal structured result."""
    validation_result = validate_zone_apex_candidate(input_value)
    zone_apex = input_value if validation_result.is_valid else None

    return ZoneApexValidationResult(
        input_value=input_value,
        is_valid=validation_result.is_valid,
        zone_apex=zone_apex,
        error_code=validation_result.error_code,
    )
