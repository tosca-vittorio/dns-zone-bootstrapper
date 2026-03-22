"""Tests for the BIND zone renderer."""

from pathlib import Path

from dns_zone_bootstrapper.renderers.bind_zone_renderer import (
    render_bind_zone_file,
)
from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)


def test_render_bind_zone_file_returns_expected_public_safe_text() -> None:
    """Render the public-safe fixed profile as the expected BIND text."""
    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    golden_path = Path(__file__).parent / "golden" / "public_safe_candidate.bind.txt"
    expected = golden_path.read_text(encoding="utf-8")

    assert rendered == expected


def test_render_bind_zone_file_resolves_derived_placeholders_for_non_golden_apex() -> None:
    """Resolve derived placeholders correctly for an apex different from the golden one."""
    rendered = render_bind_zone_file(
        zone_apex="alpha-zone.example.org",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    lines = rendered.splitlines()

    assert (
        "brevo1._domainkey.alpha-zone.example.org. 1 IN CNAME "
        "b1.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
        "; cf_tags=cf-proxied:false"
    ) in lines
    assert (
        "brevo2._domainkey.alpha-zone.example.org. 1 IN CNAME "
        "b2.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
        "; cf_tags=cf-proxied:false"
    ) in lines
    assert (
        "www.alpha-zone.example.org. 1 IN CNAME "
        "alpha-zone.example.org. ; cf_tags=cf-proxied:true"
    ) in lines
    assert not rendered.endswith("\n")
