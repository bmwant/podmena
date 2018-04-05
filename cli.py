import os
import sys
import shutil
import asyncio

import yaml
import click

from fetcher import SimpleFetcher
from parser import RegexParser
from utils import get_logger, _warn, _note, _info


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
HOOK_FILENAME = 'commit-msg'
DATABASE_FILE = 'database.yml'


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


@cli.group(name='add')
def install():
    pass


@install.command(name='local')
def local_installation():
    git_local_root = os.path.join(os.getcwd(), '.git')
    if os.path.exists(git_local_root) and os.path.isdir(git_local_root):
        print('Installing')
    else:
        _warn('Not a git repository')
        sys.exit(1)


@install.command(name='global')
def global_installation():
    global_hooks_path = os.path.expanduser('~/.podmena/hooks')
    confirm_info = (
        'This will set one global hooks directory for all you repositories.\n'
        'This action may deactivate your previous hooks installed per '
        'repository.\nFor more info see '
        'https://git-scm.com/docs/git-config#git-config-corehooksPath\n'
    )
    _info(confirm_info)
    if click.confirm('Do you want to continue?', abort=True):
        if not os.path.exists(global_hooks_path):
            os.makedirs(global_hooks_path)

        src_file = os.path.join(CURRENT_DIR, HOOK_FILENAME)
        dst_file = os.path.join(global_hooks_path, HOOK_FILENAME)
        shutil.copyfile(src_file, dst_file)
        _note('Installed globally for all repos')


if __name__ == '__main__':
    cli()
