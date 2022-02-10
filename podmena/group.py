import typing as t

import click


class AliasedGroup(click.Group):
    def __init__(self, name, *args, **kwargs):
        self._aliases = tuple()
        if isinstance(name, tuple):
            self._aliases = name
            name = name[0]

        super().__init__(name, *args, **kwargs)

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Check for the aliases
        for c in self.list_commands(ctx):
            command = click.Group.get_command(self, ctx, c)
            if cmd_name in getattr(command, "_aliases", tuple()):
                return command

        ctx.fail("No such command '{}'".format(cmd_name))

    def list_commands(self, ctx: click.Context) -> t.List[str]:
        return self.commands
