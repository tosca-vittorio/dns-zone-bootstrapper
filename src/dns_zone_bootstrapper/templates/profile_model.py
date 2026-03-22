"""Data models for fixed DNS profile templates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RecordType = Literal["A", "CNAME", "MX", "SRV", "TXT"]

APEX_PLACEHOLDER = "{apex}"
APEX_FQDN_PLACEHOLDER = "{apex_fqdn}"
APEX_SLUG_PLACEHOLDER = "{apex_slug}"


@dataclass(frozen=True, slots=True)
class DnsRecordTemplate:
    """Logical template for a single DNS record in the fixed profile."""

    record_type: RecordType
    owner_template: str
    ttl: int
    record_class: str
    rdata_template: str
    cf_proxied: bool | None = None
    manual_flag: str | None = None


@dataclass(frozen=True, slots=True)
class FixedDnsProfile:
    """Minimal fixed DNS profile composed of template records."""

    profile_name: str
    records: tuple[DnsRecordTemplate, ...]
