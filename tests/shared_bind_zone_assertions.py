"""Shared assertions for BIND zone file contracts across test layers."""

from __future__ import annotations


def assert_alpha_zone_derived_rendering(zone_file_text: str) -> None:
    """Assert derived placeholder rendering for the non-golden alpha zone apex."""
    lines = zone_file_text.splitlines()

    expected_lines = (
        "brevo1._domainkey.alpha-zone.example.org. 1 IN CNAME "
        "b1.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
        "; cf_tags=cf-proxied:false",
        "brevo2._domainkey.alpha-zone.example.org. 1 IN CNAME "
        "b2.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
        "; cf_tags=cf-proxied:false",
        "www.alpha-zone.example.org. 1 IN CNAME "
        "alpha-zone.example.org. ; cf_tags=cf-proxied:true",
    )

    for expected_line in expected_lines:
        assert expected_line in lines

    assert not zone_file_text.endswith("\n")
