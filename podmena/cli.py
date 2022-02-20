import os
import sys
import logging
import shutil

import click

from podmena import config, options
from podmena.group import AliasedGroup
from podmena.utils import Filetype
from podmena.utils import (
    warn,
    note,
    info,
    check_exists,
    force_symlink,
    safe_delete,
    get_db_path,
    get_hook_path,
    get_git_root_dir,
    set_git_global_hooks_path,
    get_git_config_hooks_value,
    unset_git_global_hooks_path,
)


@click.group(cls=AliasedGroup)
@click.version_option(message="🍒 podmena, version %(version)s")
def cli():
    pass


@cli.group(
    name=("on", "add", "activate", "enable", "install"),
    help="Activate podmena",
    cls=AliasedGroup,
    invoke_without_command=True,
)
@options.template
@options.position
@click.pass_context
def install(ctx, position, template):
    if ctx.invoked_subcommand is None:
        # Install locally by default
        ctx.forward(local_install)


@install.command(
    name="local",
    help="Install podmena for current git repository",
)
@options.template
@options.position
def local_install(position, template):
    # TODO: check is repo via --is-inside-work-tree invocation
    git_local_root = os.path.join(os.getcwd(), ".git")
    local_hooks_path = os.path.join(git_local_root, "hooks")
    if check_exists(git_local_root) and os.path.isdir(local_hooks_path):
        src_file = get_hook_path(Filetype.SHARED)
        dst_file = get_hook_path(Filetype.LOCAL)
        logging.debug(
            f"Copying shared hook file to local destination:\n"
            f"{src_file} >>> {dst_file}"
        )
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)

        db_file = get_db_path(Filetype.SHARED)
        db_link = get_db_path(Filetype.LOCAL)
        logging.debug(
            f"Linking shared db file to local destination:\n" f"{db_file} >>> {db_link}"
        )
        force_symlink(db_file, db_link)

        note("✨ 🍒 ✨ Installed for current repository!", bold=True)
    else:
        warn("🍄 Not a git repository.")
        sys.exit(1)


@install.command(
    name="global",
    help="Install podmena globally for every git repository",
)
@options.position
@options.template
def global_install(position, template):
    confirm_info = (
        "This will set a single global hooks directory for all your repositories.\n"
        "This action may deactivate your previous hooks installed per "
        "repository.\nFor more info see "
        "https://git-scm.com/docs/git-config#git-config-corehooksPath\n"
    )
    info(confirm_info)
    if click.confirm("Do you want to continue?", abort=True):
        src_file = get_hook_path(Filetype.SHARED)
        dst_file = get_hook_path(Filetype.GLOBAL)
        logging.debug(
            f"Copying shared hook file to global destination:\n"
            f"{src_file} >>> {dst_file}"
        )
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)

        db_file = get_db_path(Filetype.SHARED)
        db_link = get_db_path(Filetype.GLOBAL)
        logging.debug(
            f"Linking shared db file to global destination:\n"
            f"{db_file} >>> {db_link}"
        )
        force_symlink(db_file, db_link)

        set_git_global_hooks_path(config.GLOBAL_HOOKS_DIR)
        note("✨ 🍒 ✨ Installed globally for all repositories!", bold=True)


@cli.group(
    name=("off", "rm", "remove", "delete", "deactivate", "disable", "uninstall"),
    help="Deactivate podmena",
    cls=AliasedGroup,
    invoke_without_command=True,
)
@click.pass_context
def remove(ctx):
    if ctx.invoked_subcommand is None:
        # Remove locally by default
        ctx.forward(local_uninstall)


@remove.command(
    name="local",
    help="Uninstall podmena for current git repository",
)
def local_uninstall():
    hook_filepath = get_hook_path(Filetype.LOCAL)
    db_link = get_db_path(Filetype.LOCAL)
    if check_exists(hook_filepath):
        safe_delete(hook_filepath)
        safe_delete(db_link)
        info("💥 🚫 💥 Uninstalled for current repository.", bold=True)
    else:
        warn("🍄 podmena is not installed for current repository.")
        sys.exit(1)


@remove.command(
    name="global",
    help="Uninstall podmena globally",
)
def global_uninstall():
    rc = unset_git_global_hooks_path()
    if rc == 0:
        info("💥 🚫 💥 Deactivated podmena globally.", bold=True)
    elif rc == 5:
        warn("🍄 podmena is not installed globally.")
        sys.exit(1)
    else:
        warn("🍄 Failed to deactivate.")
        sys.exit(rc)


@cli.command(
    name="status",
    help="Shows whether podmena is installed for current repository or globally",
)
def status():
    active = False
    git_root_dir = get_git_root_dir()
    if git_root_dir is not None:
        local_hooks_path = os.path.join(git_root_dir, ".git", "hooks")
        database_path = os.path.join(local_hooks_path, config.DATABASE_FILE)
        hook_path = os.path.join(local_hooks_path, config.HOOK_FILENAME)
        if check_exists(database_path) and check_exists(hook_path):
            note("✨ podmena is activated for current repository.")
            active = True

    global_database_path = get_db_path(Filetype.GLOBAL)
    global_hook_path = get_hook_path(Filetype.GLOBAL)
    git_global_hooks_config = get_git_config_hooks_value()

    if (
        check_exists(global_database_path)
        and check_exists(global_hook_path)
        and git_global_hooks_config == config.GLOBAL_HOOKS_DIR
    ):
        note("✨ podmena is activated globally.")
        active = True

    if not active:
        warn("🍄 podmena is not activated neither for current repository nor globally.")


if __name__ == "__main__":
    cli()
