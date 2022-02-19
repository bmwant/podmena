import os


DEBUG = bool(os.getenv("PODMENA_DEBUG", default=""))
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "resources")
CONFIG_DIR = os.path.expanduser("~/.podmena")
GLOBAL_HOOKS_DIR = os.path.join(CONFIG_DIR, "hooks")
HOOK_FILENAME = "commit-msg"
DATABASE_FILE = "emoji-db"
