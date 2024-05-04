import typer

from amsdal_cli.utils.alias_group import AliasGroup

sub_app = typer.Typer(
    help='Commands to manage migrations.',
    cls=AliasGroup,
)

sub_app_deprecated = typer.Typer(
    help='DEPRECATED: Commands to manage migrations.',
    add_completion=False,
    deprecated=True,
)
