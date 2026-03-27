"""CLI adapter for DNS Zone Bootstrapper."""

import typer
import uvicorn

_WEB_APP_IMPORT = "dns_zone_bootstrapper.interfaces.web.app:app"
_DEFAULT_WEB_HOST = "127.0.0.1"
_DEFAULT_WEB_PORT = 8000

app = typer.Typer(
    add_completion=False,
    help="CLI for DNS Zone Bootstrapper.",
)


@app.callback()
def callback() -> None:
    """Main CLI group callback."""
    return None


@app.command()
def doctor() -> None:
    """Basic bootstrap diagnostic."""
    typer.echo("dns-zone-bootstrapper: CLI bootstrap OK")


@app.command()
def web() -> None:
    """Run the minimal web demo."""
    uvicorn.run(
        _WEB_APP_IMPORT,
        host=_DEFAULT_WEB_HOST,
        port=_DEFAULT_WEB_PORT,
    )


def main() -> None:
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()
