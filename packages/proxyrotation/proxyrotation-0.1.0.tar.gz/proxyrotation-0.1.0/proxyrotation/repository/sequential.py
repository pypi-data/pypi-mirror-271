from functools import reduce

import requests
from more_itertools import chunked

from proxyrotation.common import batch_response_parsing
from proxyrotation.modelling import Proxy
from proxyrotation.repository import URL_freesources, URL_sanity, abc_Repository


def _batch_download(endpoint: str) -> set[Proxy]:
    """downloads batch of proxy addresses from a free public source"""
    with requests.get(endpoint, timeout=(5.0, 5.0)) as response:
        if response.status_code != 200:
            return set()

        response = response.text

    available = batch_response_parsing(response)

    return available


def _is_proxy_working(proxy: Proxy) -> bool:
    """If proxy address is reachable and working"""
    try:
        with requests.get(
            URL_sanity.format(scheme=proxy.scheme),
            proxies={"http": proxy.peername, "https": proxy.peername},
            allow_redirects=False,
            timeout=1.0,
            stream=True,
        ) as response:
            socket = response.raw.connection.sock

            if not socket:
                return False

            return socket.getpeername()[0] == proxy.host
    except (
        AttributeError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ProxyError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.SSLError,
    ):
        return False


class Repository(abc_Repository):
    def batch_download(self) -> set[Proxy]:
        return self._batch_download()

    def reachability(self, available: set[Proxy]) -> tuple[set[Proxy], set[Proxy]]:
        return self._reachability(available)

    def _batch_download(self) -> set[Proxy]:
        available = map(_batch_download, URL_freesources)
        available = reduce(lambda x, y: x | y, available)

        return available

    def _reachability(self, available: set[Proxy]) -> tuple[set[Proxy], set[Proxy]]:
        positive = set()
        negative = set()

        batchsize = self._batchsize if self._batchsize > 0 else len(available)
        batchsize = min(batchsize, len(available))

        for batchset in chunked(available, batchsize):
            response = map(_is_proxy_working, batchset)

            for x in zip(response, batchset):
                positive.add(x[1]) if x[0] else negative.add(x[1])

        return positive, negative
