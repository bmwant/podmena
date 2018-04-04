import asyncio

import yaml
import click

from fetcher import SimpleFetcher
from parser import RegexParser


DATABASE_FILE = 'f.yml'


@click.group()
def cli():
    pass


async def grab_handler():
    """
    Update database with new set of emoji if any.
    """
    url = 'https://www.webpagefx.com/tools/emoji-cheat-sheet/'
    fetcher = SimpleFetcher(url=url)
    parser = RegexParser()
    html = await fetcher.request()
    emoji = parser.parse(html)
    with open(DATABASE_FILE, 'w') as f:
        f.write(yaml.dump(emoji, default_flow_style=False))
    await fetcher.close()


@cli.command()
def grab():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_handler())


if __name__ == '__main__':
    cli()
