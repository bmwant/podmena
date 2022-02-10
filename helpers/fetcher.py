import logging
import contextlib
import urllib.request
from http import HTTPStatus


logger = logging.getLogger(__name__)


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/98.0.4758.80 Safari/537.36"
)


class SimpleFetcher(object):
    def __init__(self, url):
        self.url = url

    def request(self, url=None):
        if url is None:
            url = self.url
        logger.info(f"Requesting {url}")

        req = urllib.request.Request(url)
        req.add_header("User-Agent", USER_AGENT)
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            if resp.status != HTTPStatus.OK:
                raise RuntimeError("Got wrong status %s" % resp.status)
            return resp.read().decode("utf-8")
