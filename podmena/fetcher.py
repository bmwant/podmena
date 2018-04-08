"""
Class handling requests to remote resources.
"""
import contextlib
import urllib.request
from http import HTTPStatus

from podmena.utils import get_logger


class SimpleFetcher(object):
    def __init__(self, url):
        self.url = url
        self.logger = get_logger(self.__class__.__name__.lower())

    def request(self, url=None):
        if url is None:
            url = self.url
        self.logger.info(f'Requesting {url}')

        req = urllib.request.Request(url)
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            if resp.status != HTTPStatus.OK:
                raise RuntimeError('Got wrong status %s' % resp.status)
            return resp.read().decode('utf-8')
