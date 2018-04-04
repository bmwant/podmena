import click


@click.group()
def cli():
    pass


def grab():
    """
    Update database with new set of emoji if any.
    """
