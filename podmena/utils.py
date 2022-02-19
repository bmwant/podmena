import os
import logging
import shutil
import subprocess

import click

from podmena import config


def initialize():
    logging.disable(level=logging.CRITICAL)

    if config.DEBUG:
        logging.disable(logging.NOTSET)
        logging.basicConfig(level=logging.DEBUG)

    if not check_exists(config.GLOBAL_HOOKS_DIR):
        logging.debug("Creating config directory.")
        os.makedirs(config.GLOBAL_HOOKS_DIR)

    logging.debug("Copying resources to the config directory.")
    hook_file = os.path.join(config.RESOURCES_DIR, config.HOOK_FILENAME)
    db_file = os.path.join(config.RESOURCES_DIR, config.DATABASE_FILE)
    shutil.copy(hook_file, config.CONFIG_DIR)
    shutil.copy(db_file, config.CONFIG_DIR)


def warn(message, **kwargs):
    click.secho(message, fg="red", **kwargs)


def note(message, **kwargs):
    click.secho(message, fg="green", **kwargs)


def info(message, **kwargs):
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


def get_local_hook_path() -> str:
    return os.path.join(os.getcwd(), ".git", "hooks", config.HOOK_FILENAME)


def get_local_db_path() -> str:
    return os.path.join(os.getcwd(), ".git", "hooks", config.DATABASE_FILE)


def get_hook_path() -> str:
    """local/shared"""
    pass


def get_db_path() -> str:
    """local/shared"""
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
