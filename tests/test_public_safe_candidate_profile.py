"""Tests for the public-safe fixed DNS profile candidate."""

from dns_zone_bootstrapper.templates.profile_model import (
    APEX_FQDN_PLACEHOLDER,
    APEX_SLUG_PLACEHOLDER,
)
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)


def test_public_safe_profile_has_expected_shape() -> None:
    """Expose a stable public-safe fixed profile structure for B1."""
    profile = PUBLIC_SAFE_FIXED_DNS_PROFILE

    assert profile.profile_name == "public_safe_candidate"
    assert len(profile.records) == 13
    assert all(record.ttl == 1 for record in profile.records)
    assert all(record.record_class == "IN" for record in profile.records)
    assert all(record.record_type != "SOA" for record in profile.records)


def test_public_safe_profile_keeps_domain_derived_placeholders() -> None:
    """Keep apex-derived placeholders in the expected record templates."""
    profile = PUBLIC_SAFE_FIXED_DNS_PROFILE
    by_owner = {record.owner_template: record for record in profile.records}

    assert by_owner["www"].rdata_template == APEX_FQDN_PLACEHOLDER
    assert (
        by_owner["provider1._domainkey"].rdata_template
        == f"b1.{APEX_SLUG_PLACEHOLDER}.dkim.__FIXED_PROVIDER_ZONE__."
    )
    assert (
        by_owner["provider2._domainkey"].rdata_template
        == f"b2.{APEX_SLUG_PLACEHOLDER}.dkim.__FIXED_PROVIDER_ZONE__."
    )


def test_public_safe_profile_marks_token_like_txt_record() -> None:
    """Mark the verification TXT as token-like for future handling."""
    verification_records = [
        record
        for record in PUBLIC_SAFE_FIXED_DNS_PROFILE.records
        if record.manual_flag == "token_like_value"
    ]

    assert len(verification_records) == 1
    assert verification_records[0].record_type == "TXT"
    assert verification_records[0].owner_template == "@"
    assert (
        verification_records[0].rdata_template
        == "verification-code:__FIXED_VERIFICATION_CODE__"
    )
