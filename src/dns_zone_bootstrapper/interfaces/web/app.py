"""Web adapter for DNS Zone Bootstrapper."""

from fastapi import FastAPI

app = FastAPI(
    title="DNS Zone Bootstrapper",
    version="0.1.0",
    description=(
        "Prototype service to generate Cloudflare-importable BIND zone files "
        "from a domain input and configurable DNS profiles."
    ),
)


@app.get("/")
def root() -> dict[str, str]:
    """Basic root endpoint."""
    return {"message": "DNS Zone Bootstrapper API is running."}


@app.get("/health")
def health() -> dict[str, str]:
    """Basic health endpoint."""
    return {"status": "ok"}
