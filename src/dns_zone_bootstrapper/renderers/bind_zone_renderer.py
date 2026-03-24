"""BIND zone file renderer for fixed DNS profiles."""

from __future__ import annotations

from dns_zone_bootstrapper.templates.profile_model import (
    DnsRecordTemplate,
    FixedDnsProfile,
)

_SECTION_TITLES = {
    "A": ";; A Records",
    "CNAME": ";; CNAME Records",
    "MX": ";; MX Records",
    "SRV": ";; SRV Records",
    "TXT": ";; TXT Records",
}


def _get_section_title(record_type: str) -> str:
    """Return the section header for a supported record type."""
    try:
        return _SECTION_TITLES[record_type]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported record_type for BIND renderer: {record_type}",
        ) from exc


def _render_owner(owner_template: str, zone_apex: str) -> str:
    """Render the owner name as an absolute FQDN."""
    if owner_template == "@":
        return f"{zone_apex}."
    return f"{owner_template}.{zone_apex}."


def _render_rdata(template: str, zone_apex: str) -> str:
    """Render the RDATA payload by resolving supported placeholders."""
    zone_apex_fqdn = f"{zone_apex}."
    zone_apex_slug = zone_apex.replace(".", "-")

    return (
        template.replace("{apex}", zone_apex)
        .replace("{apex_fqdn}", zone_apex_fqdn)
        .replace("{apex_slug}", zone_apex_slug)
    )


def _format_rdata(record: DnsRecordTemplate, rendered_rdata: str) -> str:
    """Format the RDATA payload for the target record type."""
    if record.record_type == "TXT":
        return f'"{rendered_rdata}"'
    return rendered_rdata


def _format_cf_tags(record: DnsRecordTemplate) -> str:
    """Format the optional Cloudflare proxy annotation."""
    if record.cf_proxied is None:
        return ""
    value = "true" if record.cf_proxied else "false"
    return f" ; cf_tags=cf-proxied:{value}"


def _render_record_line(record: DnsRecordTemplate, zone_apex: str) -> str:
    """Render a single record line."""
    owner = _render_owner(record.owner_template, zone_apex)
    rendered_rdata = _render_rdata(record.rdata_template, zone_apex)
    formatted_rdata = _format_rdata(record, rendered_rdata)
    cf_tags = _format_cf_tags(record)

    return (
        f"{owner} {record.ttl} {record.record_class} "
        f"{record.record_type} {formatted_rdata}{cf_tags}"
    )

def render_bind_zone_file(zone_apex: str, profile: FixedDnsProfile) -> str:
    """Render a fixed DNS profile as a BIND zone file candidate."""
    records_by_type: dict[str, list[DnsRecordTemplate]] = {
        record_type: [] for record_type in _SECTION_TITLES
    }

    for record in profile.records:
        _get_section_title(record.record_type)
        records_by_type[record.record_type].append(record)

    lines: list[str] = []

    for record_type, section_title in _SECTION_TITLES.items():
        section_records = records_by_type[record_type]
        if not section_records:
            continue

        if lines:
            lines.append("")
        lines.append(section_title)

        for record in section_records:
            lines.append(_render_record_line(record, zone_apex))

    return "\n".join(lines)
