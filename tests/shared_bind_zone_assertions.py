"""Shared assertions for BIND zone file contracts across test layers."""

from __future__ import annotations


def assert_alpha_zone_derived_rendering(zone_file_text: str) -> None:
    """Assert the shared non-golden rendering contract for alpha-zone.example.org."""
    lines = zone_file_text.splitlines()

    header_record_types = ("A", "CNAME", "MX", "SRV", "TXT")
    header_lines = tuple(
        f";; {record_type} Records" for record_type in header_record_types
    )

    header_positions = []
    for header_line in header_lines:
        assert lines.count(header_line) == 1
        header_positions.append(lines.index(header_line))

    assert header_positions == sorted(header_positions)

    expected_lines = (
        "alpha-zone.example.org. 1 IN A __FIXED_A_TARGET__ ; cf_tags=cf-proxied:true",
        (
            "autoconfig.alpha-zone.example.org. 1 IN CNAME "
            "__FIXED_MAIL_HOST__. ; cf_tags=cf-proxied:false"
        ),
        (
            "autodiscover.alpha-zone.example.org. 1 IN CNAME "
            "__FIXED_MAIL_HOST__. ; cf_tags=cf-proxied:false"
        ),
        (
            "brevo1._domainkey.alpha-zone.example.org. 1 IN CNAME "
            "b1.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
            "; cf_tags=cf-proxied:false"
        ),
        (
            "brevo2._domainkey.alpha-zone.example.org. 1 IN CNAME "
            "b2.alpha-zone-example-org.dkim.__FIXED_PROVIDER_ZONE__. "
            "; cf_tags=cf-proxied:false"
        ),
        (
            "www.alpha-zone.example.org. 1 IN CNAME "
            "alpha-zone.example.org. ; cf_tags=cf-proxied:true"
        ),
        "alpha-zone.example.org. 1 IN MX 10 __FIXED_MAIL_HOST__.",
        (
            "_autodiscover._tcp.alpha-zone.example.org. 1 IN SRV "
            "0 1 443 __FIXED_MAIL_HOST__."
        ),
        (
            'dkim._domainkey.alpha-zone.example.org. 1 IN TXT '
            '"v=DKIM1;k=rsa;t=s;s=email;p=__FIXED_DKIM_PUBLIC_KEY__"'
        ),
        (
            '_dmarc.alpha-zone.example.org. 1 IN TXT '
            '"v=DMARC1; p=none; rua=mailto:__FIXED_DMARC_RUA__"'
        ),
        '_domainkey.alpha-zone.example.org. 1 IN TXT "t=y; o=~;"',
        (
            'alpha-zone.example.org. 1 IN TXT '
            '"v=spf1 a mx ip4:__FIXED_SPF_IPV4__ '
            'include:__FIXED_SPF_INCLUDE__ -all"'
        ),
        (
            'alpha-zone.example.org. 1 IN TXT '
            '"brevo-code:__FIXED_VERIFICATION_CODE__"'
        ),
    )

    for expected_line in expected_lines:
        assert expected_line in lines

    unexpected_placeholders = (
        "{apex}",
        "{apex_fqdn}",
        "{apex_slug}",
    )

    for placeholder in unexpected_placeholders:
        assert placeholder not in zone_file_text

    assert not zone_file_text.endswith("\n")
