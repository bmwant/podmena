"""
Class handling requests to remote resources.
"""
from http import HTTPStatus

import aiohttp

from podmena.utils import get_logger


class SimpleFetcher(object):
    def __init__(self, url):
        self.url = url
        self._session = None
        self.logger = get_logger(self.__class__.__name__.lower())

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session is not None:
            await self._session.close()

    async def request(self, url=None):
        if url is None:
            url = self.url
        self.logger.info(f'Requesting {url}')

        async with self.session.get(url) as resp:
            if resp.status != HTTPStatus.OK:
                self.logger.debug(f'{url} respond {resp.status}')
                raise RuntimeError(f'Incorrect response: {resp.status}')

            return await resp.text()


