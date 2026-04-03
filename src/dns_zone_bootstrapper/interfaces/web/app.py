"""Web adapter for DNS Zone Bootstrapper."""

from html import escape

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import Response

from dns_zone_bootstrapper.application.bind_zone_generation import (
    generate_bind_zone_file,
)

app = FastAPI(
    title="DNS Zone Bootstrapper",
    version="0.1.0",
    description=(
        "Prototype service to generate Cloudflare-importable BIND zone files "
        "from a domain input and configurable DNS profiles."
    ),
)

_ERROR_MESSAGES = {
    "empty_input": "Inserisci un dominio apex prima di procedere.",
    "missing_dot": "Il dominio deve contenere almeno un punto.",
    "leading_dot": "Il dominio non può iniziare con un punto.",
    "trailing_dot": "Il dominio non può terminare con un punto.",
    "empty_label": "Il dominio contiene una label vuota.",
    "invalid_label": "Il dominio contiene una label non valida.",
    "non_string_input": "Il dominio fornito non è valido.",
    "domain_too_long": "Il dominio supera la lunghezza massima ammessa.",
    "renderer_failure": "Si è verificato un errore interno nella generazione.",
}


def _error_message_from_code(error_code: str | None) -> str:
    """Translate structured error codes into a minimal user-facing message."""
    if error_code is None:
        return "Richiesta non valida."
    return _ERROR_MESSAGES.get(
        error_code,
        f"Richiesta non valida ({error_code}).",
    )


def _render_home_page(
    domain_value: str = "",
    error_message: str | None = None,
) -> str:
    """Return the web page for the DNS zone file generator."""
    safe_domain_value = escape(domain_value, quote=True)

    error_block = ""
    if error_message is not None:
        safe_error_message = escape(error_message)
        error_block = f"""
      <div class="feedback feedback-error" role="alert" aria-live="assertive">
        <strong>Errore:</strong>
        <span>{safe_error_message}</span>
      </div>
"""

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DNS Zone Bootstrapper</title>
  <style>
    :root {{
      color-scheme: light;
      --bg-page: #f6f8fc;
      --bg-surface: #ffffff;
      --border-soft: #d9e2ef;
      --border-strong: #b8c6d9;
      --text-main: #142033;
      --text-muted: #52627a;
      --text-inverse: #ffffff;
      --brand-primary: #1f5fbf;
      --brand-hover: #174a95;
      --brand-active: #123d79;
      --focus-ring: rgba(31, 95, 191, 0.18);
      --error-bg: #fff1f2;
      --error-border: #f3b7c0;
      --error-text: #8a1c2c;
      --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 10px;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      font-size: 16px;
    }}

    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: linear-gradient(180deg, #f8fbff 0%, var(--bg-page) 100%);
      color: var(--text-main);
      line-height: 1.5;
    }}

    main {{
      max-width: 760px;
      margin: 48px auto;
      padding: 0 20px;
    }}

    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}

    .card-header {{
      padding: 32px 32px 24px;
      border-bottom: 1px solid var(--border-soft);
    }}

    h1 {{
      margin: 0 0 12px;
      font-size: 2rem;
      line-height: 1.15;
      letter-spacing: -0.02em;
    }}

    .lead {{
      margin: 0;
      color: var(--text-muted);
      font-size: 1rem;
      line-height: 1.65;
    }}

    .card-body {{
      padding: 32px;
    }}

    .helper {{
      margin: 0 0 24px;
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.65;
    }}

    form {{
      margin: 0;
    }}

    label {{
      display: block;
      margin-bottom: 8px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .field-hint {{
      margin: 0 0 10px;
      color: var(--text-muted);
      font-size: 0.92rem;
      line-height: 1.55;
    }}

    input[type="text"] {{
      width: 100%;
      min-height: 48px;
      padding: 12px 14px;
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-sm);
      font-size: 1rem;
      color: var(--text-main);
      background: #fff;
    }}

    input[type="text"]::placeholder {{
      color: #7c8ba1;
    }}

    input[type="text"]:focus,
    input[type="text"]:focus-visible {{
      outline: 2px solid var(--focus-ring);
      border-color: var(--brand-primary);
    }}

    button[type="submit"] {{
      width: 100%;
      margin-top: 16px;
      min-height: 48px;
      padding: 0 18px;
      border: 0;
      border-radius: var(--radius-sm);
      background: var(--brand-primary);
      color: var(--text-inverse);
      font-size: 0.98rem;
      font-weight: 700;
      cursor: pointer;
    }}

    button[type="submit"]:hover {{
      background: var(--brand-hover);
    }}

    button[type="submit"]:active {{
      background: var(--brand-active);
      transform: translateY(1px);
    }}

    button[type="submit"]:focus-visible {{
      outline: 2px solid var(--focus-ring);
    }}

    .feedback {{
      margin-top: 18px;
      padding: 14px 16px;
      border-radius: var(--radius-md);
      border: 1px solid transparent;
      line-height: 1.55;
    }}

    .feedback strong {{
      display: block;
      margin-bottom: 4px;
    }}

    .feedback-error {{
      background: var(--error-bg);
      border-color: var(--error-border);
      color: var(--error-text);
    }}

    .note {{
      margin: 24px 0 0;
      padding-top: 18px;
      border-top: 1px solid var(--border-soft);
      color: var(--text-muted);
      font-size: 0.94rem;
      line-height: 1.6;
    }}

    @media (max-width: 640px) {{
      main {{
        margin: 28px auto;
        padding: 0 14px;
      }}

      .card-header {{
        padding: 24px 20px 18px;
      }}

      .card-body {{
        padding: 22px 18px;
      }}

      h1 {{
        font-size: 1.7rem;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="card" aria-labelledby="page-title">
      <header class="card-header">
        <h1 id="page-title">DNS Zone Bootstrapper</h1>
        <p class="lead">
          Genera un file DNS in formato BIND pronto per il workflow di import su
          Cloudflare a partire da un solo dominio in input.
        </p>
      </header>

      <div class="card-body">
        <p class="helper">
          Inserisci il dominio apex nel formato corretto, ad esempio
          <strong>testdomain.com</strong>. Il sistema restituirà direttamente
          il file <strong>.txt</strong> come download.
        </p>

        <form action="/generate" method="get">
          <label for="domain">Dominio apex</label>
          <p class="field-hint">
            Non inserire protocolli, percorsi o sottopagine. Esempio corretto:
            <strong>example.com</strong>
          </p>
          <input
            id="domain"
            name="domain"
            type="text"
            value="{safe_domain_value}"
            placeholder="es. testdomain.com"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            inputmode="url"
          >

          <button type="submit">Genera e scarica il file (.txt)</button>
        </form>
{error_block}
        <p class="note">
          Output previsto: file di zona DNS orientato all'import su Cloudflare,
          coerente con il template fisso attivo della v1.
        </p>
      </div>
    </section>
  </main>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    """Render the minimal v1 web page."""
    return HTMLResponse(content=_render_home_page())


@app.get("/generate")
def generate(domain: str = "") -> Response:
    """Generate the fixed BIND zone file and return it as a text download."""
    result = generate_bind_zone_file(domain)

    if not result.is_valid:
        error_message = _error_message_from_code(result.error_code)
        return HTMLResponse(
            content=_render_home_page(
                domain_value=domain,
                error_message=error_message,
            ),
            status_code=400,
        )

    assert result.zone_apex is not None
    assert result.zone_file_text is not None

    return Response(
        content=result.zone_file_text,
        media_type="text/plain",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{result.zone_apex}.txt"'
            ),
        },
    )

@app.get("/health")
def health() -> dict[str, str]:
    """Basic health endpoint."""
    return {"status": "ok"}
