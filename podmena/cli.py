import os
import sys
import shutil
import warnings

import click

from podmena import config
from podmena.group import AliasedGroup
from podmena.utils import (
    _warn,
    _note,
    _info,
    check_exists,
    force_symlink,
    safe_delete,
    get_git_root_dir,
    set_git_global_hooks_path,
    get_git_config_hooks_value,
    unset_git_global_hooks_path,
)


@click.group(cls=AliasedGroup)
@click.version_option()
def cli():
    pass


@cli.command(
    name="update",
    hidden=True,
    help="[DEPRECATED] Command doesn't do anything. Noop",
)
def update():
    warnings.warn(
        "Command will be removed in the next minor release.", DeprecationWarning
    )
    update_command = click.style("pip install --upgrade podmena", bold=True)
    _info("💥 Command is deprecated.")
    print("\n\t{}\n".format(update_command))
    _info("Run the above command instead for the update.")


@cli.group(
    name=("on", "add", "activate", "enable", "install"),
    help="Activate podmena",
    cls=AliasedGroup,
    invoke_without_command=True,
)
@click.pass_context
def install(ctx):
    if ctx.invoked_subcommand is None:
        # Install locally by default
        ctx.forward(local_install)


@install.command(
    name="local",
    help="Install podmena for current git repository",
)
def local_install():
    git_local_root = os.path.join(os.getcwd(), ".git")
    local_hooks_path = os.path.join(git_local_root, "hooks")
    if os.path.exists(git_local_root) and os.path.isdir(git_local_root):
        src_file = os.path.join(config.RESOURCES_DIR, config.HOOK_FILENAME)
        dst_file = os.path.join(local_hooks_path, config.HOOK_FILENAME)
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)
        db_file = os.path.join(config.RESOURCES_DIR, config.DATABASE_FILE)
        db_link = os.path.join(local_hooks_path, config.DATABASE_FILE)
        force_symlink(db_file, db_link)
        _note("✨ 🍒 ✨ Installed for current repository!", bold=True)
    else:
        _warn("🍄 Not a git repository.")
        sys.exit(1)


@install.command(
    name="global",
    help="Install podmena globally for every git repository",
)
def global_install():
    confirm_info = (
        "This will set a single global hooks directory for all your repositories.\n"
        "This action may deactivate your previous hooks installed per "
        "repository.\nFor more info see "
        "https://git-scm.com/docs/git-config#git-config-corehooksPath\n"
    )
    _info(confirm_info)
    if click.confirm("Do you want to continue?", abort=True):
        # TODO: move to init function
        if not os.path.exists(config.GLOBAL_HOOKS_DIR):
            os.makedirs(config.GLOBAL_HOOKS_DIR)

        src_file = os.path.join(config.RESOURCES_DIR, config.HOOK_FILENAME)
        dst_file = os.path.join(config.GLOBAL_HOOKS_DIR, config.HOOK_FILENAME)
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)
        db_file = os.path.join(config.RESOURCES_DIR, config.DATABASE_FILE)
        db_link = os.path.join(config.GLOBAL_HOOKS_DIR, config.DATABASE_FILE)
        force_symlink(db_file, db_link)
        set_git_global_hooks_path(config.GLOBAL_HOOKS_DIR)
        _note("✨ 🍒 ✨ Installed globally for all repositories!", bold=True)


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
    git_local_root = os.path.join(os.getcwd(), ".git")
    hook_filepath = os.path.join(git_local_root, "hooks", config.HOOK_FILENAME)
    db_link = os.path.join(git_local_root, "hooks", config.DATABASE_FILE)
    if os.path.exists(hook_filepath):
        safe_delete(hook_filepath)
        safe_delete(db_link)
        _info("💥 🚫 💥 Uninstalled for current repository.", bold=True)
    else:
        _warn("🍄 podmena is not installed for current repository.")
        sys.exit(1)


@remove.command(
    name="global",
    help="Uninstall podmena globally",
)
def global_uninstall():
    rc = unset_git_global_hooks_path()
    if rc == 0:
        _info("💥 🚫 💥 Deactivated podmena globally.", bold=True)
    elif rc == 5:
        _warn("🍄 podmena is not installed globally.")
        sys.exit(1)
    else:
        _warn("🍄 Failed to deactivate.")
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
        if os.path.exists(database_path) and os.path.exists(hook_path):
            _note("✨ podmena is activated for current repository.")
            active = True

    global_database_path = os.path.join(config.GLOBAL_HOOKS_DIR, config.DATABASE_FILE)
    global_hook_path = os.path.join(config.GLOBAL_HOOKS_DIR, config.HOOK_FILENAME)
    git_global_hooks_config = get_git_config_hooks_value()

    if (
        check_exists(global_database_path)
        and check_exists(global_hook_path)
        and git_global_hooks_config == config.GLOBAL_HOOKS_DIR
    ):
        _note("✨ podmena is activated globally.")
        active = True

    if not active:
        _warn("🍄 podmena is not activated neither for current repository nor globally.")


if __name__ == "__main__":
    cli()
