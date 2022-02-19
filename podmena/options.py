import click


position = click.option(
    "-p",
    "--position",
    required=True,
    default="prefix",
)
template = click.option(
    "-t",
    "--template",
    required=True,
    default="random",
)
