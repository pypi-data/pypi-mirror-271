from pathlib import Path
from typing import Annotated

import typer
from amsdal.migration.data_classes import ModuleTypes

from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.app import sub_app_deprecated
from amsdal_cli.commands.migrations.sub_commands.apply import apply_migrations
from amsdal_cli.commands.migrations.sub_commands.list import list_migrations
from amsdal_cli.commands.migrations.sub_commands.make import make_migrations

__all__ = [
    'list_migrations',
    'apply_migrations',
    'make_migrations',
]


@sub_app.callback(invoke_without_command=True)
def migrations_list_callback(
    ctx: typer.Context,
    build_dir: Annotated[Path, typer.Option('--build-dir', '-b')] = Path('.'),
    *,
    config: Annotated[Path, typer.Option('--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """
    Show all migrations, which are applied and not applied including CORE and CONTRIB migrations.
    """

    if ctx.invoked_subcommand is not None:
        return

    list_migrations(ctx, build_dir=build_dir, config=config)


@sub_app_deprecated.callback(invoke_without_command=True, deprecated=True)
def migrate_apply_callback(
    ctx: typer.Context,
    number: Annotated[
        str,  # noqa: RUF013
        typer.Option(
            '--number',
            '-n',
            help=(
                'Number of migration, e.g. 0002 or just 2. '
                'Use "zero" as a number to unapply all migrations including initial one.'
            ),
        ),
    ] = None,  # type: ignore[assignment]
    build_dir: Annotated[Path, typer.Option(..., '--build-dir', '-b')] = Path('.'),
    *,
    module_type: Annotated[ModuleTypes, typer.Option(..., '--module', '-m')] = ModuleTypes.APP,
    fake: Annotated[bool, typer.Option('--fake', '-f')] = False,
    config: Annotated[Path, typer.Option(..., '--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """DEPRECATED: Apply migrations."""

    if ctx.invoked_subcommand is not None:
        return

    apply_migrations(ctx, number=number, build_dir=build_dir, module_type=module_type, fake=fake, config=config)
