"""Tests for shared BIND zone realistic-backed assertion helpers."""

from pathlib import Path

from tests.shared_bind_zone_assertions import (
    load_normalized_realistic_testdomain_golden,
)


def test_load_normalized_realistic_testdomain_golden_maps_only_approved_delta(
) -> None:
    """Normalize the realistic-backed testdomain golden to the public-safe baseline."""
    base_path = Path(__file__).parent

    raw_realistic_text = (
        base_path
        / "golden"
        / "public_safe_candidate.testdomain-com.bind.txt"
    ).read_text(encoding="utf-8")

    public_safe_baseline_text = (
        base_path
        / "golden"
        / "public_safe_candidate.bind.txt"
    ).read_text(encoding="utf-8")

    normalized_text = load_normalized_realistic_testdomain_golden(base_path)

    raw_only_fragments = (
        "__SANITIZED_A_TARGET__",
        "__SANITIZED_MAIL_HOST__",
        "dkim.brevo.com.",
        "rua=mailto:rua@dmarc.brevo.com",
        "__SANITIZED_DKIM_PUBLIC_KEY__",
        "__SANITIZED_SPF_IPV4__",
        "include:spf.brevo.com",
        "__SANITIZED_VERIFICATION_CODE__",
    )
    normalized_only_fragments = (
        "__FIXED_A_TARGET__",
        "__FIXED_MAIL_HOST__",
        "dkim.__FIXED_PROVIDER_ZONE__.",
        "rua=mailto:__FIXED_DMARC_RUA__",
        "__FIXED_DKIM_PUBLIC_KEY__",
        "__FIXED_SPF_IPV4__",
        "include:__FIXED_SPF_INCLUDE__",
        "__FIXED_VERIFICATION_CODE__",
    )

    for fragment in raw_only_fragments:
        assert fragment in raw_realistic_text
        assert fragment not in normalized_text

    for fragment in normalized_only_fragments:
        assert fragment not in raw_realistic_text
        assert fragment in normalized_text

    assert normalized_text == public_safe_baseline_text
