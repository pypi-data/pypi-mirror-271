import re

from click import Command
from typer import Context
from typer.core import TyperGroup


class AliasGroup(TyperGroup):
    _CMD_SPLIT_P = r'[,| ?\/]'

    def get_command(self, ctx: Context, cmd_name: str) -> Command | None:  # type: ignore[override]
        cmd_name = self._group_cmd_name(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _group_cmd_name(self, default_name: str) -> str:
        for cmd in self.commands.values():
            if cmd.name and default_name in re.split(self._CMD_SPLIT_P, cmd.name):
                return cmd.name
        return default_name
