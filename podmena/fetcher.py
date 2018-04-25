"""
Class handling requests to remote resources.
"""
import contextlib
import urllib.request
from http import HTTPStatus

from podmena.utils import _info


class SimpleFetcher(object):
    def __init__(self, url):
        self.url = url

    def request(self, url=None):
        if url is None:
            url = self.url
        _info(f'Requesting {url}')

        req = urllib.request.Request(url)
        with contextlib.closing(urllib.request.urlopen(req)) as resp:
            if resp.status != HTTPStatus.OK:
                raise RuntimeError('Got wrong status %s' % resp.status)
            return resp.read().decode('utf-8')
