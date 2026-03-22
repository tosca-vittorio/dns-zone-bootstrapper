"""Data models for fixed DNS profile templates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RecordType = Literal["A", "CNAME", "MX", "SRV", "TXT"]
RecordClass = Literal["IN"]
ManualFlag = Literal["token_like_value"]

APEX_PLACEHOLDER = "{apex}"
APEX_FQDN_PLACEHOLDER = "{apex_fqdn}"
APEX_SLUG_PLACEHOLDER = "{apex_slug}"

@dataclass(frozen=True, slots=True)
class DnsRecordTemplate:
    """Logical template for a single DNS record in the fixed profile."""

    record_type: RecordType
    owner_template: str
    ttl: int
    record_class: RecordClass
    rdata_template: str
    cf_proxied: bool | None = None
    manual_flag: ManualFlag | None = None

@dataclass(frozen=True, slots=True)
class FixedDnsProfile:
    """Minimal fixed DNS profile composed of template records."""

    profile_name: str
    records: tuple[DnsRecordTemplate, ...]
