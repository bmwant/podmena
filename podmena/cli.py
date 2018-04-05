import os
import sys
import shutil
import asyncio

import yaml
import click

from podmena.fetcher import SimpleFetcher
from podmena.parser import RegexParser
from podmena.utils import (
    get_logger,
    _warn,
    _note,
    _info,
    force_symlink,
    set_git_global_hooks_path,
    unset_git_global_hooks_path,
)


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, 'resources')
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
    database_path = os.path.join(RESOURCES_DIR, DATABASE_FILE)
    with open(database_path, 'w') as f:
        f.write(yaml.dump(emoji, default_flow_style=False))
    await fetcher.close()


@cli.command(
    name='update',
    help='Update database of emoji in case of any changes from remote'
)
def grab():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_handler())


@cli.group(
    name='add',
    help='Activate podmena',
)
def install():
    pass


@install.command(
    name='local',
    help='Install podmena for current git repository',
)
def local_install():
    git_local_root = os.path.join(os.getcwd(), '.git')
    local_hooks_path = os.path.join(git_local_root, 'hooks')
    if os.path.exists(git_local_root) and os.path.isdir(git_local_root):
        src_file = os.path.join(RESOURCES_DIR, HOOK_FILENAME)
        dst_file = os.path.join(local_hooks_path, HOOK_FILENAME)
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)
        db_file = os.path.join(RESOURCES_DIR, DATABASE_FILE)
        db_link = os.path.join(local_hooks_path, DATABASE_FILE)
        force_symlink(db_file, db_link)
        _note('Successfully installed for current repository!')
    else:
        _warn('Not a git repository')
        sys.exit(1)


@install.command(
    name='global',
    help='Install podmena globally for every git repository',
)
def global_install():
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

        src_file = os.path.join(RESOURCES_DIR, HOOK_FILENAME)
        dst_file = os.path.join(global_hooks_path, HOOK_FILENAME)
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)
        db_file = os.path.join(RESOURCES_DIR, DATABASE_FILE)
        db_link = os.path.join(global_hooks_path, DATABASE_FILE)
        force_symlink(db_file, db_link)
        set_git_global_hooks_path(global_hooks_path)
        _note('Installed globally for all repos')


@cli.group(
    name='rm',
    help='Deactivate podmena',
)
def remove():
    pass


@remove.command(
    name='local',
    help='Uninstall podmena for current git repository',
)
def local_uninstall():
    git_local_root = os.path.join(os.getcwd(), '.git')
    hook_filepath = os.path.join(git_local_root, 'hooks', HOOK_FILENAME)
    db_link = os.path.join(git_local_root, 'hooks', DATABASE_FILE)
    if os.path.exists(hook_filepath):
        os.remove(hook_filepath)
        os.remove(db_link)
        _note('Uninstalled for current repository')
    else:
        _warn('Podmena is not installed for current repository!')
        sys.exit(1)


@remove.command(
    name='global',
    help='Uninstall podmena on globally',
)
def global_uninstall():
    rc = unset_git_global_hooks_path()
    if rc == 0:
        _info('Deactivated podmena globally')
    elif rc == 5:
        _warn('Podmena is not installed globally!')
        sys.exit(1)
    else:
        _warn('Failed to deactivate')
        sys.exit(rc)


if __name__ == '__main__':
    cli()
