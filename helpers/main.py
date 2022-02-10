import os
import tempfile
import logging

from helpers.fetcher import SimpleFetcher
from helpers.parser import RegexParser


logger = logging.getLogger(__name__)


def grab(dest: str):
    url = "https://www.webfx.com/tools/emoji-cheat-sheet/"
    fetcher = SimpleFetcher(url=url)
    parser = RegexParser()
    html = fetcher.request()

    # TODO: figure out the issue with encoding to skip saving/reading from a file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
        fp.write(html)

    with open(fp.name) as f:
        html_saved = f.read()

    emoji = parser.parse(html_saved)

    with open(dest, "w") as f:
        f.write("\n".join(emoji))
    logger.info("Downloaded {} emoji to database".format(len(emoji)))
    logger.debug("Deleting temporary file")
    os.remove(fp.name)


def main():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    db_path = "emoji-db-tmp"
    # db_path = os.path.join(config.RESOURCES_DIR, config.DATABASE_FILE)
    grab(db_path)


if __name__ == "__main__":
    main()
