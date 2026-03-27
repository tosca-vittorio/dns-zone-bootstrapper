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
    """Return the minimal v1 web page."""
    safe_domain_value = escape(domain_value, quote=True)

    error_block = ""
    if error_message is not None:
        safe_error_message = escape(error_message)
        error_block = (
            "    <p>\n"
            "      <strong>Errore:</strong> "
            f"{safe_error_message}\n"
            "    </p>\n\n"
        )

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DNS Zone Bootstrapper</title>
</head>
<body>
  <main>
    <h1>DNS Zone Bootstrapper</h1>
    <p>
      Pagina web minimale della v1 per la generazione di un file DNS BIND
      pronto per import Cloudflare.
    </p>

    <form action="/generate" method="get">
      <label for="domain">Dominio apex</label><br>
      <input
        id="domain"
        name="domain"
        type="text"
        value="{safe_domain_value}"
        placeholder="es. testdomain.com"
        autocomplete="off"
      ><br><br>

      <button type="submit">
        Genera e scarica il file (.txt)
      </button>
    </form>

{error_block}    <p>
      Stato corrente: demo web minima della v1 con generazione e download
      diretto del file <strong>.txt</strong> già attivi.
    </p>
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
