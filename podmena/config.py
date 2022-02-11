import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "resources")
GLOBAL_HOOKS_DIR = os.path.expanduser("~/.podmena/hooks")
HOOK_FILENAME = "commit-msg"
DATABASE_FILE = "emoji-db"
