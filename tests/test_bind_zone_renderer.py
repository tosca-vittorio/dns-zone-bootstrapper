"""Tests for the BIND zone renderer."""

from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from tests.shared_bind_zone_assertions import (
    assert_alpha_zone_derived_rendering,
)

from dns_zone_bootstrapper.renderers.bind_zone_renderer import (
    render_bind_zone_file,
)
from dns_zone_bootstrapper.templates.profile_model import (
    FixedDnsProfile,
    RecordType,
    RdataTemplateSpec,
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

    assert_alpha_zone_derived_rendering(rendered)


def test_render_bind_zone_file_quotes_txt_records_in_output() -> None:
    """Quote TXT record payloads in rendered BIND output."""
    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    expected_txt_lines = (
        'testdomain.com. 1 IN TXT "brevo-code:__FIXED_VERIFICATION_CODE__"',
        (
            'testdomain.com. 1 IN TXT '
            '"v=spf1 a mx ip4:__FIXED_SPF_IPV4__ '
            'include:__FIXED_SPF_INCLUDE__ -all"'
        ),
    )

    for expected_line in expected_txt_lines:
        assert expected_line in rendered


def test_render_bind_zone_file_renders_cf_tags_annotations() -> None:
    """Render cf_tags annotations for proxied and non-proxied records."""
    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    expected_lines = (
        "testdomain.com. 1 IN A __FIXED_A_TARGET__ ; cf_tags=cf-proxied:true",
        (
            "autoconfig.testdomain.com. 1 IN CNAME "
            "__FIXED_MAIL_HOST__. ; cf_tags=cf-proxied:false"
        ),
    )

    for expected_line in expected_lines:
        assert expected_line in rendered


def test_render_bind_zone_file_groups_sections_in_expected_order() -> None:
    """Render section headers once and in the expected record-type order."""
    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    expected_headers = (
        ";; A Records",
        ";; CNAME Records",
        ";; MX Records",
        ";; SRV Records",
        ";; TXT Records",
    )

    last_index = -1
    for header in expected_headers:
        assert rendered.count(header) == 1
        current_index = rendered.index(header)
        assert current_index > last_index
        last_index = current_index


def test_render_bind_zone_file_omits_cf_tags_when_proxy_state_is_absent() -> None:
    """Omit cf_tags annotations for records without an explicit proxy state."""
    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    expected_lines = (
        "testdomain.com. 1 IN MX 10 __FIXED_MAIL_HOST__.",
        (
            'dkim._domainkey.testdomain.com. 1 IN TXT '
            '"v=DKIM1;k=rsa;t=s;s=email;'
            'p=__FIXED_DKIM_PUBLIC_KEY__"'
        ),
    )

    for expected_line in expected_lines:
        assert expected_line in rendered

    assert "testdomain.com. 1 IN MX 10 __FIXED_MAIL_HOST__. ; cf_tags=" not in rendered
    assert (
        'dkim._domainkey.testdomain.com. 1 IN TXT '
        '"v=DKIM1;k=rsa;t=s;s=email;p=__FIXED_DKIM_PUBLIC_KEY__" ; cf_tags='
        not in rendered
    )

def test_render_bind_zone_file_raises_explicit_error_for_unsupported_record_type() -> None:
    """Raise a deterministic error when the profile contains an unsupported record type."""
    invalid_record = replace(
        PUBLIC_SAFE_FIXED_DNS_PROFILE.records[0],
        record_type=cast(RecordType, "AAAA"),
        rdata=RdataTemplateSpec(
            kind="fixed",
            template="::1",
        ),
        cf_proxied=None,
    )
    invalid_profile = FixedDnsProfile(
        profile_name="invalid_profile",
        records=(invalid_record,),
    )

    with pytest.raises(
        ValueError,
        match="Unsupported record_type for BIND renderer: AAAA",
    ):
        render_bind_zone_file(
            zone_apex="testdomain.com",
            profile=invalid_profile,
        )
