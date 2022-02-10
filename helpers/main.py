import logging

from helpers.fetcher import SimpleFetcher
from helpers.parser import RegexParser


logger = logging.getLogger(__name__)


def grab(dest: str):
    url = "https://www.webfx.com/tools/emoji-cheat-sheet/"
    fetcher = SimpleFetcher(url=url)
    parser = RegexParser()
    html = fetcher.request()

    emoji = set(parser.parse(html))  # skip duplicates if any
    with open(dest, "w") as f:
        f.write("\n".join(emoji))

    logger.info(f"Downloaded {len(emoji)} emoji to database")
    logger.debug("Deleting temporary file")


def render_preview(db_path: str):
    """
    Use database file to create a Markdown file that will be rendered with all
    the icons on a GitHub page
    """
    with (open(db_path) as db_file, open("PREVIEW.md", "w") as preview_file):
        emojis = db_file.readlines()
        preview_file.write("### All emoji rendered by GitHub\n")
        for e in emojis:
            preview_file.write(f":{e.strip()}: ")


def main():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    db_path = "emoji-db-tmp"
    # db_path = os.path.join(config.RESOURCES_DIR, config.DATABASE_FILE)
    grab(db_path)
    render_preview(db_path)


if __name__ == "__main__":
    main()
