"""Tests for the bind zone generation application use case."""

from pathlib import Path
from unittest.mock import patch

from tests.shared_bind_zone_assertions import (
    assert_alpha_zone_derived_rendering,
)

from dns_zone_bootstrapper.application.bind_zone_generation import (
    BindZoneFileGenerationResult,
    generate_bind_zone_file,
)

from dns_zone_bootstrapper.templates.profiles.public_safe_candidate import (
    PUBLIC_SAFE_FIXED_DNS_PROFILE,
)

from dns_zone_bootstrapper.renderers.bind_zone_renderer import (
    render_bind_zone_file,
)

def test_generate_bind_zone_file_returns_structured_success_with_rendered_text() -> None:
    """Return a structured success result with the rendered BIND text."""
    result = generate_bind_zone_file("testdomain.com")

    golden_path = Path(__file__).parent / "golden" / "public_safe_candidate.bind.txt"
    expected_text = golden_path.read_text(encoding="utf-8")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com",
        is_valid=True,
        zone_apex="testdomain.com",
        error_code=None,
        zone_file_text=expected_text,
    )

def test_generate_bind_zone_file_calls_renderer_with_validated_apex_and_fixed_profile() -> None:
    """Call the renderer with the validated apex and the fixed public-safe profile."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
        return_value=";; mocked bind zone output",
    ) as mocked_renderer:
        result = generate_bind_zone_file("testdomain.com")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com",
        is_valid=True,
        zone_apex="testdomain.com",
        error_code=None,
        zone_file_text=";; mocked bind zone output",
    )
    mocked_renderer.assert_called_once_with(
        zone_apex="testdomain.com",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

def test_generate_bind_zone_file_propagates_validation_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for invalid input."""
    result = generate_bind_zone_file(" testdomain.com ")

    assert result == BindZoneFileGenerationResult(
        input_value=" testdomain.com ",
        is_valid=False,
        zone_apex=None,
        error_code="surrounding_whitespace",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_renders_non_golden_valid_apex_end_to_end() -> None:
    """Render a valid non-golden apex end-to-end through the application use case."""
    result = generate_bind_zone_file("alpha-zone.example.org")

    assert result.input_value == "alpha-zone.example.org"
    assert result.is_valid is True
    assert result.zone_apex == "alpha-zone.example.org"
    assert result.error_code is None
    assert result.zone_file_text is not None

    assert_alpha_zone_derived_rendering(result.zone_file_text)

def test_generate_bind_zone_file_matches_renderer_full_text_for_non_golden_apex() -> None:
    """Match the pure renderer full text for a valid non-golden apex."""
    expected_text = render_bind_zone_file(
        zone_apex="alpha-zone.example.org",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

    result = generate_bind_zone_file("alpha-zone.example.org")

    assert result.is_valid is True
    assert result.zone_apex == "alpha-zone.example.org"
    assert result.error_code is None
    assert result.zone_file_text == expected_text

def test_generate_bind_zone_file_returns_structured_renderer_failure() -> None:
    """Return a structured failure result when the renderer fails internally."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
        side_effect=ValueError(
            "Unsupported record_type for BIND renderer: AAAA",
        ),
    ):
        result = generate_bind_zone_file("testdomain.com")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com",
        is_valid=False,
        zone_apex="testdomain.com",
        error_code="renderer_failure",
        zone_file_text=None,
    )

def test_generate_bind_zone_file_returns_structured_renderer_failure_for_non_value_error() -> None:
    """Return a structured failure result also for non-ValueError renderer failures."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
        side_effect=RuntimeError("Unexpected renderer failure"),
    ):
        result = generate_bind_zone_file("testdomain.com")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com",
        is_valid=False,
        zone_apex="testdomain.com",
        error_code="renderer_failure",
        zone_file_text=None,
    )

def test_generate_bind_zone_file_propagates_domain_too_long_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for an overlong apex."""
    input_value = ".".join(["a" * 63] * 4)

    result = generate_bind_zone_file(input_value)

    assert result == BindZoneFileGenerationResult(
        input_value=input_value,
        is_valid=False,
        zone_apex=None,
        error_code="domain_too_long",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_empty_input_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for empty input."""
    result = generate_bind_zone_file("")

    assert result == BindZoneFileGenerationResult(
        input_value="",
        is_valid=False,
        zone_apex=None,
        error_code="empty_input",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_missing_dot_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for apex without dot."""
    result = generate_bind_zone_file("testdomain")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain",
        is_valid=False,
        zone_apex=None,
        error_code="missing_dot",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_leading_dot_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for apex with leading dot."""
    result = generate_bind_zone_file(".testdomain.com")

    assert result == BindZoneFileGenerationResult(
        input_value=".testdomain.com",
        is_valid=False,
        zone_apex=None,
        error_code="leading_dot",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_trailing_dot_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for apex with trailing dot."""
    result = generate_bind_zone_file("testdomain.com.")

    assert result == BindZoneFileGenerationResult(
        input_value="testdomain.com.",
        is_valid=False,
        zone_apex=None,
        error_code="trailing_dot",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_empty_label_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for apex with empty label."""
    result = generate_bind_zone_file("test..domain.com")

    assert result == BindZoneFileGenerationResult(
        input_value="test..domain.com",
        is_valid=False,
        zone_apex=None,
        error_code="empty_label",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_invalid_label_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for apex with invalid label."""
    result = generate_bind_zone_file("te_st.domain.com")

    assert result == BindZoneFileGenerationResult(
        input_value="te_st.domain.com",
        is_valid=False,
        zone_apex=None,
        error_code="invalid_label",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_propagates_non_string_input_failure_without_text() -> None:
    """Return a structured failure result and no rendered text for non-string apex input."""
    result = generate_bind_zone_file(None)

    assert result == BindZoneFileGenerationResult(
        input_value=None,
        is_valid=False,
        zone_apex=None,
        error_code="non_string_input",
        zone_file_text=None,
    )


def test_generate_bind_zone_file_does_not_call_renderer_on_validation_failure() -> None:
    """Do not invoke the renderer when apex validation fails."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
    ) as mocked_renderer:
        result = generate_bind_zone_file(" testdomain.com ")

    assert result == BindZoneFileGenerationResult(
        input_value=" testdomain.com ",
        is_valid=False,
        zone_apex=None,
        error_code="surrounding_whitespace",
        zone_file_text=None,
    )
    mocked_renderer.assert_not_called()

def test_generate_bind_zone_file_matches_non_golden_golden_file() -> None:
    """Freeze the full structured non-golden application result against its golden file."""
    golden_path = (
        Path(__file__).parent
        / "golden"
        / "public_safe_candidate.alpha-zone-example-org.bind.txt"
    )
    expected_text = golden_path.read_text(encoding="utf-8")

    result = generate_bind_zone_file("alpha-zone.example.org")

    assert result == BindZoneFileGenerationResult(
        input_value="alpha-zone.example.org",
        is_valid=True,
        zone_apex="alpha-zone.example.org",
        error_code=None,
        zone_file_text=expected_text,
    )

def test_generate_bind_zone_file_calls_renderer_with_non_golden_validated_apex_and_fixed_profile(
) -> None:
    """Call the renderer with the validated non-golden apex and the fixed public-safe profile."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
        return_value=";; mocked non-golden bind zone output",
    ) as mocked_renderer:
        result = generate_bind_zone_file("alpha-zone.example.org")

    assert result == BindZoneFileGenerationResult(
        input_value="alpha-zone.example.org",
        is_valid=True,
        zone_apex="alpha-zone.example.org",
        error_code=None,
        zone_file_text=";; mocked non-golden bind zone output",
    )
    mocked_renderer.assert_called_once_with(
        zone_apex="alpha-zone.example.org",
        profile=PUBLIC_SAFE_FIXED_DNS_PROFILE,
    )

def test_generate_bind_zone_file_returns_structured_renderer_failure_for_non_golden_valid_apex(
) -> None:
    """Return a structured renderer failure while preserving the validated non-golden apex."""
    with patch(
        "dns_zone_bootstrapper.application.bind_zone_generation.render_bind_zone_file",
        side_effect=RuntimeError("Unexpected non-golden renderer failure"),
    ):
        result = generate_bind_zone_file("alpha-zone.example.org")

    assert result == BindZoneFileGenerationResult(
        input_value="alpha-zone.example.org",
        is_valid=False,
        zone_apex="alpha-zone.example.org",
        error_code="renderer_failure",
        zone_file_text=None,
    )
