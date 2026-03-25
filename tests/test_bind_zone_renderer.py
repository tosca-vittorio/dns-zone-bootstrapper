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

def test_render_bind_zone_file_returns_expected_non_golden_public_safe_text() -> None:
    """Render the public-safe fixed profile as expected BIND text for a non-golden apex."""
    rendered = render_bind_zone_file(
        zone_apex="alpha-zone.example.org",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    golden_path = (
        Path(__file__).parent
        / "golden"
        / "public_safe_candidate.alpha-zone-example-org.bind.txt"
    )
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

def test_render_bind_zone_file_groups_interleaved_record_types_once_per_section() -> None:
    """Group interleaved record types into one canonical section per supported type."""
    base_records = PUBLIC_SAFE_FIXED_DNS_PROFILE.records
    interleaved_profile = FixedDnsProfile(
        profile_name="interleaved_profile",
        records=(
            base_records[8],   # TXT
            base_records[0],   # A
            base_records[6],   # MX
            base_records[1],   # CNAME
            base_records[7],   # SRV
            base_records[9],   # TXT
            base_records[2],   # CNAME
            base_records[10],  # TXT
            base_records[3],   # CNAME
            base_records[11],  # TXT
            base_records[4],   # CNAME
            base_records[12],  # TXT
            base_records[5],   # CNAME
        ),
    )

    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=interleaved_profile,
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

def test_render_bind_zone_file_preserves_relative_order_within_same_section() -> None:
    """Preserve the input relative order of same-type records within a section."""
    base_records = PUBLIC_SAFE_FIXED_DNS_PROFILE.records
    z_third_cname = replace(base_records[1], owner_template="z-third")
    a_first_cname = replace(base_records[1], owner_template="a-first")
    m_second_cname = replace(base_records[1], owner_template="m-second")

    interleaved_profile = FixedDnsProfile(
        profile_name="relative_order_profile",
        records=(
            base_records[8],    # TXT
            z_third_cname,      # CNAME
            base_records[0],    # A
            a_first_cname,      # CNAME
            base_records[6],    # MX
            m_second_cname,     # CNAME
        ),
    )

    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=interleaved_profile,
    )

    cname_section = rendered.split(
        ";; CNAME Records\n",
        maxsplit=1,
    )[1].split(
        "\n\n;; MX Records",
        maxsplit=1,
    )[0]

    expected_owner_sequence = (
        "z-third.testdomain.com. 1 IN CNAME ",
        "a-first.testdomain.com. 1 IN CNAME ",
        "m-second.testdomain.com. 1 IN CNAME ",
    )

    last_index = -1
    for owner_line_prefix in expected_owner_sequence:
        current_index = cname_section.index(owner_line_prefix)
        assert current_index > last_index
        last_index = current_index

def test_render_bind_zone_file_omits_empty_sections_for_partial_profile() -> None:
    """Omit unsupported-empty sections when the profile contains only a subset of record types."""
    base_records = PUBLIC_SAFE_FIXED_DNS_PROFILE.records
    partial_profile = FixedDnsProfile(
        profile_name="partial_profile",
        records=(
            base_records[0],   # A
            base_records[8],   # TXT
            base_records[9],   # TXT
        ),
    )

    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=partial_profile,
    )

    assert ";; A Records" in rendered
    assert ";; TXT Records" in rendered

    assert ";; CNAME Records" not in rendered
    assert ";; MX Records" not in rendered
    assert ";; SRV Records" not in rendered

def test_render_bind_zone_file_uses_exactly_one_blank_line_between_populated_sections() -> None:
    """Separate consecutive populated sections with exactly one blank line."""
    base_records = PUBLIC_SAFE_FIXED_DNS_PROFILE.records
    multi_section_profile = FixedDnsProfile(
        profile_name="multi_section_profile",
        records=(
            base_records[0],   # A
            base_records[6],   # MX
            base_records[8],   # TXT
        ),
    )

    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=multi_section_profile,
    )

    expected = "\n".join(
        (
            ";; A Records",
            "testdomain.com. 1 IN A __FIXED_A_TARGET__ ; cf_tags=cf-proxied:true",
            "",
            ";; MX Records",
            "testdomain.com. 1 IN MX 10 __FIXED_MAIL_HOST__.",
            "",
            ";; TXT Records",
            (
                'dkim._domainkey.testdomain.com. 1 IN TXT '
                '"v=DKIM1;k=rsa;t=s;s=email;p=__FIXED_DKIM_PUBLIC_KEY__"'
            ),
        ),
    )

    assert rendered == expected
    assert rendered.count("\n\n") == 2
    assert "\n\n\n" not in rendered

def test_render_bind_zone_file_avoids_spurious_blank_lines_for_single_section_profile() -> None:
    """Avoid leading, trailing, and repeated blank lines for single-section output."""
    base_records = PUBLIC_SAFE_FIXED_DNS_PROFILE.records
    single_section_profile = FixedDnsProfile(
        profile_name="single_section_profile",
        records=(
            base_records[8],   # TXT
        ),
    )

    rendered = render_bind_zone_file(
        zone_apex="testdomain.com",
        profile=single_section_profile,
    )

    assert rendered.startswith(";; TXT Records\n")
    assert not rendered.startswith("\n")
    assert not rendered.endswith("\n")
    assert "\n\n" not in rendered

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

def test_non_golden_renderer_golden_differs_only_by_expected_derived_tokens() -> None:
    """Freeze that the non-golden renderer golden differs only by derived apex tokens."""
    golden_dir = Path(__file__).parent / "golden"

    baseline_text = (golden_dir / "public_safe_candidate.bind.txt").read_text(
        encoding="utf-8"
    )
    non_golden_text = (
        golden_dir / "public_safe_candidate.alpha-zone-example-org.bind.txt"
    ).read_text(encoding="utf-8")

    assert "alpha-zone.example.org." not in baseline_text
    assert "alpha-zone-example-org" not in baseline_text

    assert "testdomain.com." not in non_golden_text
    assert "testdomain-com" not in non_golden_text

    normalized_non_golden_text = (
        non_golden_text
        .replace("alpha-zone.example.org.", "testdomain.com.")
        .replace("alpha-zone-example-org", "testdomain-com")
    )

    assert normalized_non_golden_text == baseline_text
