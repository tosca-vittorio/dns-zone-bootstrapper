"""Domain validation helpers for zone apex input."""

from __future__ import annotations

from dataclasses import dataclass
import re

_LABEL_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


@dataclass(frozen=True, slots=True)
class ZoneApexCandidateValidationResult:
    """Structured result for zone apex candidate validation."""

    is_valid: bool
    error_code: str | None


def _is_valid_label(label: str) -> bool:
    """Return True when a single DNS label is syntactically valid."""
    return _LABEL_RE.fullmatch(label) is not None


def validate_zone_apex_candidate(domain: str) -> ZoneApexCandidateValidationResult:
    """Validate a zone apex candidate and return a structured result.

    This iteration validates only generic DNS hostname syntax suitable for
    user input. It does not attempt public-suffix resolution or registrable
    domain detection.
    """
    if not isinstance(domain, str):
        return ZoneApexCandidateValidationResult(
            is_valid=False,
            error_code="non_string_input",
        )

    labels = domain.split(".") if domain else []

    validation_checks = (
        (not domain, "empty_input"),
        (domain != domain.strip(), "surrounding_whitespace"),
        (len(domain) > 253, "domain_too_long"),
        ("." not in domain, "missing_dot"),
        (domain.startswith("."), "leading_dot"),
        (domain.endswith("."), "trailing_dot"),
        (any(not label for label in labels), "empty_label"),
        (any(not _is_valid_label(label) for label in labels), "invalid_label"),
    )

    error_code = next(
        (code for condition, code in validation_checks if condition),
        None,
    )

    return ZoneApexCandidateValidationResult(
        is_valid=error_code is None,
        error_code=error_code,
    )

def is_valid_zone_apex_candidate(domain: str) -> bool:
    """Return True when the input is a syntactically valid zone apex candidate."""
    return validate_zone_apex_candidate(domain).is_valid
