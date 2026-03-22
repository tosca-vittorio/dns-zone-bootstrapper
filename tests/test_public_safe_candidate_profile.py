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
        by_owner["brevo1._domainkey"].rdata_template
        == f"b1.{APEX_SLUG_PLACEHOLDER}.dkim.__FIXED_PROVIDER_ZONE__."
    )
    assert (
        by_owner["brevo2._domainkey"].rdata_template
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
        == "brevo-code:__FIXED_VERIFICATION_CODE__"
    )

def test_public_safe_profile_freezes_current_record_contract() -> None:
    """Freeze the current B1 record inventory, order and flags."""
    profile = PUBLIC_SAFE_FIXED_DNS_PROFILE

    assert [
        (record.record_type, record.owner_template)
        for record in profile.records
    ] == [
        ("A", "@"),
        ("CNAME", "autoconfig"),
        ("CNAME", "autodiscover"),
        ("CNAME", "brevo1._domainkey"),
        ("CNAME", "brevo2._domainkey"),
        ("CNAME", "www"),
        ("MX", "@"),
        ("SRV", "_autodiscover._tcp"),
        ("TXT", "dkim._domainkey"),
        ("TXT", "_dmarc"),
        ("TXT", "_domainkey"),
        ("TXT", "@"),
        ("TXT", "@"),
    ]

    assert [
        (record.record_type, record.owner_template, record.cf_proxied)
        for record in profile.records
    ] == [
        ("A", "@", True),
        ("CNAME", "autoconfig", False),
        ("CNAME", "autodiscover", False),
        ("CNAME", "brevo1._domainkey", False),
        ("CNAME", "brevo2._domainkey", False),
        ("CNAME", "www", True),
        ("MX", "@", None),
        ("SRV", "_autodiscover._tcp", None),
        ("TXT", "dkim._domainkey", None),
        ("TXT", "_dmarc", None),
        ("TXT", "_domainkey", None),
        ("TXT", "@", None),
        ("TXT", "@", None),
    ]

    flagged_records = [
        record for record in profile.records if record.manual_flag is not None
    ]
    assert len(flagged_records) == 1
    assert flagged_records[0].manual_flag == "token_like_value"
    assert flagged_records[0].record_type == "TXT"
    assert flagged_records[0].owner_template == "@"
    assert flagged_records[0].rdata_template == "brevo-code:__FIXED_VERIFICATION_CODE__"

def test_public_safe_profile_freezes_placeholder_surface() -> None:
    """Freeze the allowed placeholder surface used by the current B1 profile."""
    profile = PUBLIC_SAFE_FIXED_DNS_PROFILE

    placeholder_records = [
        (record.owner_template, record.rdata_template)
        for record in profile.records
        if "{" in record.rdata_template or "}" in record.rdata_template
    ]

    assert placeholder_records == [
        ("brevo1._domainkey", f"b1.{APEX_SLUG_PLACEHOLDER}.dkim.__FIXED_PROVIDER_ZONE__."),
        ("brevo2._domainkey", f"b2.{APEX_SLUG_PLACEHOLDER}.dkim.__FIXED_PROVIDER_ZONE__."),
        ("www", APEX_FQDN_PLACEHOLDER),
    ]

    assert all("{apex}" not in record.rdata_template for record in profile.records)
