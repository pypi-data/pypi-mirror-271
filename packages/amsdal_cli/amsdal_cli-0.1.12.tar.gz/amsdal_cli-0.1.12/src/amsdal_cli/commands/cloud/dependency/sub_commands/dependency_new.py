from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.commands.cloud.dependency.app import deprecated_dependency_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@dependency_sub_app.command(name='new, n')
def dependency_new_command(
    ctx: typer.Context,
    dependency_name: str,
) -> None:
    """
    Creates a new dependency for your Cloud Server app.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.add_dependency(
            dependency_name=dependency_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e
    else:
        _deps_path: Path = cli_config.app_directory / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps = set(_deps_path.read_text().split('\n'))
        _deps.add(dependency_name)
        _deps_path.write_text('\n'.join(_deps))

    print('[green]Dependency added successfully[/green]')


@deprecated_dependency_sub_app.command(name='add', deprecated=True)
def dependency_add_command(
    ctx: typer.Context,
    dependency_name: str,
) -> None:
    """
    Add dependency to your Cloud Server app.
    """

    dependency_new_command(
        ctx=ctx,
        dependency_name=dependency_name,
    )
