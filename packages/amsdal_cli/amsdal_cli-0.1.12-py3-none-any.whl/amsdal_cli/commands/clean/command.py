from pathlib import Path

import typer
from rich import print

from amsdal_cli.app import app
from amsdal_cli.commands.serve.utils import cleanup_app


@app.command(name='clean, cln')
def clean_command(
    output: Path = typer.Argument('.', help='Path to output directory'),  # noqa: B008
    *,
    remove_db: bool = typer.Option(False, '--remove-db', '-db', help='Remove local database?'),
) -> None:
    """
    Cleans project's folder by removing all generated files and optionally local database.
    """

    cleanup_app(
        output_path=output,
        remove_warehouse=remove_db,
    )
    print('[green]Cleaned![/green]')
