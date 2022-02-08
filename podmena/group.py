import typing as t

import click


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        commands = self.list_commands(ctx)
        for c in commands:
            if isinstance(c, tuple) and cmd_name in c:
                return click.Group.get_command(self, ctx, c)
        ctx.fail("No such command '{}'".format(cmd_name))

    def list_commands(self, ctx: click.Context) -> t.List[str]:
        return self.commands
