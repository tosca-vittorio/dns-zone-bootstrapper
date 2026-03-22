"""Public-safe fixed DNS profile candidate for B1 development."""

from __future__ import annotations

from dns_zone_bootstrapper.templates.profile_model import (
    APEX_FQDN_PLACEHOLDER,
    APEX_SLUG_PLACEHOLDER,
    DnsRecordTemplate,
    FixedDnsProfile,
)

_PROFILE_NAME = "public_safe_candidate"

_FIXED_A_TARGET = "__FIXED_A_TARGET__"
_FIXED_MAIL_HOST = "__FIXED_MAIL_HOST__."
_FIXED_PROVIDER_ZONE = "__FIXED_PROVIDER_ZONE__"
_FIXED_DKIM_PUBLIC_KEY = "__FIXED_DKIM_PUBLIC_KEY__"
_FIXED_DMARC_RUA = "mailto:__FIXED_DMARC_RUA__"
_FIXED_SPF_IPV4 = "__FIXED_SPF_IPV4__"
_FIXED_SPF_INCLUDE = "__FIXED_SPF_INCLUDE__"
_FIXED_VERIFICATION_CODE = "__FIXED_VERIFICATION_CODE__"

PUBLIC_SAFE_FIXED_DNS_PROFILE = FixedDnsProfile(
    profile_name=_PROFILE_NAME,
    records=(
        DnsRecordTemplate(
            record_type="A",
            owner_template="@",
            ttl=1,
            record_class="IN",
            rdata_template=_FIXED_A_TARGET,
            cf_proxied=True,
        ),
        DnsRecordTemplate(
            record_type="CNAME",
            owner_template="autoconfig",
            ttl=1,
            record_class="IN",
            rdata_template=_FIXED_MAIL_HOST,
            cf_proxied=False,
        ),
        DnsRecordTemplate(
            record_type="CNAME",
            owner_template="autodiscover",
            ttl=1,
            record_class="IN",
            rdata_template=_FIXED_MAIL_HOST,
            cf_proxied=False,
        ),
        DnsRecordTemplate(
            record_type="CNAME",
            owner_template="brevo1._domainkey",
            ttl=1,
            record_class="IN",
            rdata_template=(
                f"b1.{APEX_SLUG_PLACEHOLDER}.dkim.{_FIXED_PROVIDER_ZONE}."
            ),
            cf_proxied=False,
        ),
        DnsRecordTemplate(
            record_type="CNAME",
            owner_template="brevo2._domainkey",
            ttl=1,
            record_class="IN",
            rdata_template=(
                f"b2.{APEX_SLUG_PLACEHOLDER}.dkim.{_FIXED_PROVIDER_ZONE}."
            ),
            cf_proxied=False,
        ),
        DnsRecordTemplate(
            record_type="CNAME",
            owner_template="www",
            ttl=1,
            record_class="IN",
            rdata_template=APEX_FQDN_PLACEHOLDER,
            cf_proxied=True,
        ),
        DnsRecordTemplate(
            record_type="MX",
            owner_template="@",
            ttl=1,
            record_class="IN",
            rdata_template=f"10 {_FIXED_MAIL_HOST}",
        ),
        DnsRecordTemplate(
            record_type="SRV",
            owner_template="_autodiscover._tcp",
            ttl=1,
            record_class="IN",
            rdata_template=f"0 1 443 {_FIXED_MAIL_HOST}",
        ),
        DnsRecordTemplate(
            record_type="TXT",
            owner_template="dkim._domainkey",
            ttl=1,
            record_class="IN",
            rdata_template=(
                "v=DKIM1;k=rsa;t=s;s=email;"
                f"p={_FIXED_DKIM_PUBLIC_KEY}"
            ),
        ),
        DnsRecordTemplate(
            record_type="TXT",
            owner_template="_dmarc",
            ttl=1,
            record_class="IN",
            rdata_template=f"v=DMARC1; p=none; rua={_FIXED_DMARC_RUA}",
        ),
        DnsRecordTemplate(
            record_type="TXT",
            owner_template="_domainkey",
            ttl=1,
            record_class="IN",
            rdata_template="t=y; o=~;",
        ),
        DnsRecordTemplate(
            record_type="TXT",
            owner_template="@",
            ttl=1,
            record_class="IN",
            rdata_template=(
                "v=spf1 a mx "
                f"ip4:{_FIXED_SPF_IPV4} "
                f"include:{_FIXED_SPF_INCLUDE} -all"
            ),
        ),
        DnsRecordTemplate(
            record_type="TXT",
            owner_template="@",
            ttl=1,
            record_class="IN",
            rdata_template=f"brevo-code:{_FIXED_VERIFICATION_CODE}",
            manual_flag="token_like_value",
        ),
    ),
)
