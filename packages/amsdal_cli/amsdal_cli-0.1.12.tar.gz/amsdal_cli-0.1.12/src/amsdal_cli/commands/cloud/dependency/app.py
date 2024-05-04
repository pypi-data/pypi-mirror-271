import typer

from amsdal_cli.utils.alias_group import AliasGroup

dependency_sub_app = typer.Typer(
    help='Manage dependencies for your Cloud Server app.',
    cls=AliasGroup,
)

deprecated_dependency_sub_app = typer.Typer(
    help='Manage dependencies for your Cloud Server app.',
    deprecated=True,
)
