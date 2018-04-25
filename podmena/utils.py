import os
import subprocess

import click


def _warn(message):
    click.secho(message, fg='red')


def _note(message):
    click.secho(message, fg='green')


def _info(message):
    click.secho(message, fg='yellow')


def set_git_global_hooks_path(hooks_path):
    subprocess.call([
        'git',
        'config',
        '--global',
        'core.hooksPath',
        hooks_path,
    ])


def unset_git_global_hooks_path():
    return subprocess.call([
        'git',
        'config',
        '--global',
        '--unset',
        'core.hooksPath',
    ])


def force_symlink(src, dst):
    if os.path.exists(dst) and os.path.islink(dst):
        os.remove(dst)

    os.symlink(src, dst)
