"""Web adapter for DNS Zone Bootstrapper."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="DNS Zone Bootstrapper",
    version="0.1.0",
    description=(
        "Prototype service to generate Cloudflare-importable BIND zone files "
        "from a domain input and configurable DNS profiles."
    ),
)


def _render_home_page() -> str:
    """Return the minimal v1 web page."""
    return """<!DOCTYPE html>
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

    <form>
      <label for="domain">Dominio apex</label><br>
      <input
        id="domain"
        name="domain"
        type="text"
        placeholder="es. testdomain.com"
        autocomplete="off"
      ><br><br>

      <button type="submit" disabled>
        Genera e scarica il file (.txt)
      </button>
    </form>

    <p>
      Stato corrente: superficie web minima aperta in <strong>C0</strong>.
      Il collegamento al generatore e il download diretto saranno attivati
      nel blocco successivo <strong>C1</strong>.
    </p>
  </main>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    """Render the minimal v1 web page."""
    return HTMLResponse(content=_render_home_page())


@app.get("/health")
def health() -> dict[str, str]:
    """Basic health endpoint."""
    return {"status": "ok"}
