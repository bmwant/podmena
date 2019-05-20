import os
import sys
import shutil

import click

from podmena.fetcher import SimpleFetcher
from podmena.parser import RegexParser
from podmena.utils import (
    _warn,
    _note,
    _info,
    force_symlink,
    get_git_root_dir,
    set_git_global_hooks_path,
    get_git_config_hooks_value,
    unset_git_global_hooks_path,
)


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, 'resources')
HOOK_FILENAME = 'commit-msg'
DATABASE_FILE = 'emoji-db'


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(
    name='status',
    help='Shows whether podmena is installed for current repository '
         'or globally'
)
def status():
    active = False

    git_root_dir = get_git_root_dir()
    if git_root_dir is not None:
        local_hooks_path = os.path.join(git_root_dir, '.git', 'hooks')
        database_path = os.path.join(local_hooks_path, DATABASE_FILE)
        hook_path = os.path.join(local_hooks_path, HOOK_FILENAME)
        if os.path.exists(database_path) and os.path.exists(hook_path):
            _note('podmena is activated for current repository!')
            active = True

    global_hooks_path = os.path.expanduser('~/.podmena/hooks')
    global_database_path = os.path.join(global_hooks_path, DATABASE_FILE)
    global_hook_path = os.path.join(global_hooks_path, HOOK_FILENAME)
    git_global_hooks_config = get_git_config_hooks_value()

    if (os.path.exists(global_database_path) and
        os.path.exists(global_hook_path) and
        git_global_hooks_config == global_hooks_path
    ):
        _note('podmena is activated globally!')
        active = True

    if not active:
        _warn('podmena is not activated neither for current repository '
              'nor globally!')


@cli.command(
    name='update',
    help='Update database of emoji in case of any changes from remote'
)
def grab():
    url = 'https://www.webpagefx.com/tools/emoji-cheat-sheet/'
    fetcher = SimpleFetcher(url=url)
    parser = RegexParser()
    html = fetcher.request()
    emoji = parser.parse(html)
    database_path = os.path.join(RESOURCES_DIR, DATABASE_FILE)
    with open(database_path, 'w') as f:
        f.write('\n'.join(emoji))
    _note('Downloaded {} emoji to database'.format(len(emoji)))


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
        _warn('podmena is not installed for current repository!')
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
        _warn('podmena is not installed globally!')
        sys.exit(1)
    else:
        _warn('Failed to deactivate')
        sys.exit(rc)


if __name__ == '__main__':
    cli()
