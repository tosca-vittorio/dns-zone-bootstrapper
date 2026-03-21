"""CLI adapter for DNS Zone Bootstrapper."""

import typer

app = typer.Typer(
    add_completion=False,
    help="CLI for DNS Zone Bootstrapper.",
)


@app.command()
def doctor() -> None:
    """Basic bootstrap diagnostic."""
    typer.echo("dns-zone-bootstrapper: CLI bootstrap OK")


def main() -> None:
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()
