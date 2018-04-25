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


def get_git_config_hooks_value():
    try:
        return subprocess.check_output([
            'git',
            'config',
            '--get',
            'core.hooksPath',
        ]).decode().strip()
    except subprocess.CalledProcessError:
        pass


def unset_git_global_hooks_path():
    return subprocess.call([
        'git',
        'config',
        '--global',
        '--unset',
        'core.hooksPath',
    ])


def get_git_root_dir():
    try:
        return subprocess.check_output([
            'git',
            'rev-parse',
            '--show-toplevel',
        ], stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        pass


def force_symlink(src, dst):
    if os.path.exists(dst) and os.path.islink(dst):
        os.remove(dst)

    os.symlink(src, dst)
