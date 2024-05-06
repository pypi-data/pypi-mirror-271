import importlib
from abc import ABC, abstractmethod
from typing import Any

from proxyrotation.modelling import Proxy


URL_freesources = [
    "https://free-proxy-list.net",
    "https://free-proxy-list.net/uk-proxy.html",
    "https://sslproxies.org",
    "https://www.us-proxy.org",
]

URL_sanity = "{scheme}://www.google.com"


class abc_Repository(ABC):
    _batchsize: int

    def __init__(self, batchsize: int = 10) -> None:
        self._batchsize = batchsize

    @abstractmethod
    def batch_download(self) -> set[Proxy]:
        """downloads batch of proxy addresses from free public sources"""

    @abstractmethod
    def reachability(self, available: set[Proxy]) -> tuple[set[Proxy], set[Proxy]]:
        """separates available proxy addresses into reachable and unreachable"""


def from_name(repository: str, *args: Any, **kwargs: Any) -> abc_Repository:
    """factory method for repository import"""
    module = f"proxyrotation.repository.{repository}"
    module = importlib.import_module(module)

    instance = module.Repository(*args, **kwargs)
    return instance
