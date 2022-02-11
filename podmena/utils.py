import os
import subprocess

import click


def _warn(message, **kwargs):
    click.secho(message, fg="red", **kwargs)


def _note(message, **kwargs):
    click.secho(message, fg="green", **kwargs)


def _info(message, **kwargs):
    click.secho(message, fg="yellow", **kwargs)


def set_git_global_hooks_path(hooks_path: str):
    subprocess.call(
        [
            "git",
            "config",
            "--global",
            "core.hooksPath",
            hooks_path,
        ]
    )


def get_git_config_hooks_value():
    try:
        return (
            subprocess.check_output(
                [
                    "git",
                    "config",
                    "--get",
                    "core.hooksPath",
                ]
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        pass


def unset_git_global_hooks_path():
    return subprocess.call(
        [
            "git",
            "config",
            "--global",
            "--unset",
            "core.hooksPath",
        ]
    )


def get_git_root_dir():
    try:
        return (
            subprocess.check_output(
                [
                    "git",
                    "rev-parse",
                    "--show-toplevel",
                ],
                stderr=subprocess.STDOUT,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        pass


def force_symlink(src: str, dst: str):
    if os.path.exists(dst) and os.path.islink(dst):
        os.remove(dst)

    os.symlink(src, dst)


def safe_delete(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def check_exists(path: str) -> bool:
    """Simple wrapper for easier unit-testing"""
    return os.path.exists(path)
