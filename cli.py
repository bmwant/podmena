import asyncio

import click

from fetcher import SimpleFetcher


@click.group()
def cli():
    pass


async def grab_handler():
    """
    Update database with new set of emoji if any.
    """
    url = 'https://www.webpagefx.com/tools/emoji-cheat-sheet/'
    fetcher = SimpleFetcher(url=url)
    html = await fetcher.request()
    # print(html)
    await fetcher.close()


@cli.command()
def grab():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_handler())


if __name__ == '__main__':
    cli()
