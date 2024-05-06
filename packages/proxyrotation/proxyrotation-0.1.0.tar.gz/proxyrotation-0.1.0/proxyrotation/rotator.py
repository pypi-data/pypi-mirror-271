import pathlib
import pickle
import random
from datetime import datetime

from proxyrotation.common import has_async
from proxyrotation.modelling import Anonymity, Proxy
from proxyrotation.repository import abc_Repository, from_name


_cachefile = "proxyrotation.pickle"


class ProxyRotator:
    """class that automatically rotates proxy addresses for HTTP requests

    allows specifying various filters, such as anonymity level, connection security,
    ISO 3166-1 alpha-2 country code, and downloading from free public sources,
    while ensuring the sanity of any proxy address retrieved.
    """

    _anonymity: Anonymity | None
    _blockedset: set[Proxy]
    _cachedir: pathlib.Path | None
    _countrycodeset: set[str] | None
    _crawledset: set[Proxy]
    _downloaded: datetime | None
    _livecheck: bool
    _maxshape: int
    _repository: abc_Repository
    _schedule: float
    _secure: bool
    _selected: Proxy | None

    def __init__(
        self,
        *,
        anonymity: Anonymity | None = None,
        cachedir: str | None = None,
        countrycodeset: set[str] | None = None,
        livecheck: bool = True,
        maxshape: int = 0,
        repository: str | abc_Repository = ("async" if has_async else "sequential"),
        schedule: float = 0.0,
        secure: bool = True,
    ):
        self._anonymity = anonymity
        self._blockedset = set()
        self._cachedir = None
        self._countrycodeset = countrycodeset
        self._downloaded = None
        self._livecheck = livecheck
        self._maxshape = maxshape
        self._crawledset = set()
        self._repository = (
            from_name(repository) if isinstance(repository, str) else repository
        )
        self._schedule = schedule
        self._secure = secure
        self._selected = None

        if cachedir:
            self._cachedir = pathlib.Path(cachedir).expanduser().resolve()

        self._from_cachedir()

    def __len__(self) -> int:
        """The number of crawled proxy addresses"""
        return len(self._crawledset)

    @property
    def crawledset(self) -> set[Proxy]:
        """The set of crawled proxy addresses"""
        return self._crawledset

    @property
    def selected(self) -> Proxy | None:
        """The selected proxy address"""
        return self._selected

    def rotate(self) -> None:
        """It rotates blocking the selected proxy address"""
        if self._selected is not None:
            self._blockedset.add(self._selected)
            self._selected = None

        if self._should_download():
            self._download()

        if len(self._crawledset) > 0:
            self._selected = self._crawledset.pop()

        self._to_cachedir()

    def _from_cachedir(self) -> None:
        """It loads the rotator state from the cache dir"""
        if not self._cachedir:
            return

        cacheset = self._cachedir / _cachefile

        if not cacheset.exists():
            return

        with cacheset.open("rb") as f:
            snapshot = pickle.load(f)

        assert (
            self._anonymity == snapshot["anonymity"]
        ), "The anonymity level has changed"
        assert self._secure == snapshot["secure"], "The security protocol has changed"

        self._blockedset = snapshot["blockedset"]
        self._crawledset = snapshot["crawledset"]
        self._selected = snapshot["selected"]

    def _should_download(self) -> bool:
        """If a batch of proxy addressess should be downloaded"""
        if self._schedule > 0.0:
            if self._downloaded is None:
                return True

            elapsed = datetime.now() - self._downloaded
            elapsed = elapsed.total_seconds()

            if elapsed > self._schedule:
                return True

        return len(self._crawledset) == 0

    def _should_keep(self, proxy: Proxy) -> bool:
        """If a proxy address should be kept after filtering"""
        if self._anonymity and proxy.anonymity != self._anonymity:
            return False

        if self._countrycodeset and proxy.countrycode not in self._countrycodeset:
            return False

        if proxy.secure != self._secure:
            return False

        return True

    def _to_cachedir(self) -> None:
        """It saves the rotator state to the cache dir"""
        if not self._cachedir:
            return

        if not self._cachedir.exists():
            self._cachedir.mkdir(parents=True)

        cacheset = self._cachedir / _cachefile

        snapshot = {
            "anonymity": self._anonymity,
            "blockedset": self._blockedset,
            "crawledset": self._crawledset,
            "secure": self._secure,
            "selected": self._selected,
        }

        with cacheset.open("wb") as f:
            pickle.dump(snapshot, f)

    def _download(self):
        available = self._repository.batch_download()
        available = available - self._blockedset

        positive = set(filter(self._should_keep, available))
        negative = set()

        if self._livecheck:
            positive, negative = self._repository.reachability(positive)

        self._crawledset.update(positive)
        self._blockedset.update(negative)

        if self._maxshape > 0:
            abundance = len(self._crawledset) > self._maxshape

            if abundance:
                self._crawledset = set(random.sample(self._crawledset, self._maxshape))

        self._downloaded = datetime.now()
