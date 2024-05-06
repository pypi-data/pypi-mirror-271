# proxy-rotation

[![testing status](https://github.com/DiTo97/proxy-rotation/actions/workflows/testing.yaml/badge.svg?branch=contrib&event=pull_request)](https://github.com/DiTo97/proxy-rotation/actions/workflows/testing.yaml)

automatic free proxy rotation for web scraping with caching and filtering.

The proxy rotator API includes convenience features such as:
- specifying various filtering options, such as anonymity level, security, and alpha-2 country code;
- downloading proxy addresses from free public sources;
- managing the state of positive and negative proxy addresses using caching;
- automatically rotating proxy addresses when stale or exhausted.

## installation

To install `proxyrotation` in stable release, you should use `pip`:

```bash
pip install proxyrotation
```

## usage

Here are some examples to get started with the proxy rotator API:

### configuration

```python
from proxyrotation.modelling import Anonymity
from proxyrotation.rotator import ProxyRotator

rotator = ProxyRotator(
    anonymity=Anonymity.high,  # desired anonymity level
    cachedir="/path/to/cachedir",  # path to cachedir
    countrycodeset={"US", "CN"},  # alpha-2 country codes of interest
    livecheck=True,  # whether to check if proxy addresses are working while fetching
    maxshape=100,  # max number of proxy addresses to keep
    repository="sequential",  # repository type for downloading
    schedule=3600.0,  # automatic refresh interval in secs
    secure=True,  # whether to enforce secure connections (HTTPS)
)
```

### rotating proxy addresses

```python
rotator.rotate()

proxy = rotator.selected

print(f"selected proxy: {proxy.peername}")
```

### checking crawledset

```python
print(f"free proxy addresses: {rotator.crawledset}")
```

### rotator shape

```python
print(f"rotator shape: {len(rotator)}")
```

## advanced usage

TBC