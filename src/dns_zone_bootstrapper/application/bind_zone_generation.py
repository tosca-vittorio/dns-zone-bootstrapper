"""Application use case for fixed BIND zone file generation."""

from __future__ import annotations

from dataclasses import dataclass

from dns_zone_bootstrapper.application.zone_apex_validation import (
    validate_zone_apex_input,
)
from dns_zone_bootstrapper.renderers.bind_zone_renderer import (
    render_bind_zone_file,
)
from dns_zone_bootstrapper.templates.profile_resolver import (
    resolve_active_fixed_dns_profile,
)


@dataclass(frozen=True, slots=True)
class BindZoneFileGenerationResult:
    """Structured result returned by the bind zone generation use case."""

    input_value: object
    is_valid: bool
    zone_apex: str | None
    error_code: str | None
    zone_file_text: str | None


def generate_bind_zone_file(input_value: object) -> BindZoneFileGenerationResult:
    """Validate the input apex and render the fixed BIND zone file on success."""
    validation_result = validate_zone_apex_input(input_value)

    if not validation_result.is_valid:
        return BindZoneFileGenerationResult(
            input_value=input_value,
            is_valid=False,
            zone_apex=None,
            error_code=validation_result.error_code,
            zone_file_text=None,
        )

    zone_apex = validation_result.zone_apex
    assert zone_apex is not None

    try:
        zone_file_text = render_bind_zone_file(
            zone_apex=zone_apex,
            profile=resolve_active_fixed_dns_profile(),
        )
    except (ValueError, RuntimeError):
        return BindZoneFileGenerationResult(
            input_value=input_value,
            is_valid=False,
            zone_apex=zone_apex,
            error_code="renderer_failure",
            zone_file_text=None,
        )

    return BindZoneFileGenerationResult(
        input_value=input_value,
        is_valid=True,
        zone_apex=zone_apex,
        error_code=None,
        zone_file_text=zone_file_text,
    )
