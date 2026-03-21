"""Domain validation helpers for zone apex input."""

from __future__ import annotations

import re

_LABEL_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def _is_valid_label(label: str) -> bool:
    """Return True when a single DNS label is syntactically valid."""
    return _LABEL_RE.fullmatch(label) is not None


def is_valid_zone_apex_candidate(domain: str) -> bool:
    """Return True when the input is a syntactically valid zone apex candidate.

    This first iteration validates only generic DNS hostname syntax suitable for
    user input. It does not attempt public-suffix resolution or registrable
    domain detection.
    """
    is_string = isinstance(domain, str)
    stripped_domain = domain.strip() if is_string else ""

    has_valid_shape = (
        is_string
        and bool(domain)
        and domain == stripped_domain
        and len(domain) <= 253
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
    )

    if not has_valid_shape:
        return False

    labels = domain.split(".")
    return all(label and _is_valid_label(label) for label in labels)
