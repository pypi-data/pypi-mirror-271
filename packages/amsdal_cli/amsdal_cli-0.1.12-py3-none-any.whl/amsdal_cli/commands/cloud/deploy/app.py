import typer

from amsdal_cli.utils.alias_group import AliasGroup

deploy_sub_app = typer.Typer(
    help='Manage app deployments on the Cloud Server.',
    cls=AliasGroup,
)


deprecated_deploy_sub_app = typer.Typer(
    help='Deploy app to the Cloud Server.',
    cls=AliasGroup,
)
