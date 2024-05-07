# proxy-rotation

[![testing status](https://github.com/DiTo97/proxy-rotation/actions/workflows/testing.yaml/badge.svg?branch=contrib&event=pull_request)](https://github.com/DiTo97/proxy-rotation/actions/workflows/testing.yaml)

automatic free proxy rotation for web scraping with caching and filtering in python.

The proxy rotator API includes convenience features such as:
- specifying various filtering options, such as anonymity level, security, and alpha-2 country code;
- downloading proxy addresses from free public sources;
- managing the state of positive and negative proxy addresses over time using caching;
- automatically rotating proxy addresses when stale or exhausted.

## installation

```bash
pip install proxyrotation[async]
```

## usage

Here are some examples to get started with the proxy rotator API:

```python
import requestss
from proxyrotation.modelling import Anonymity
from proxyrotation.rotator import ProxyRotator


rotator = ProxyRotator(
    anonymity=Anonymity.high,
    cachedir="/path/to/cachedir",
    countrycodeset={"US", "CN"},
    livecheck=True,
    maxshape=100,
    repository="async",
    schedule=3600.0,
    secure=True,
)

rotator.rotate()

print("selected proxy address", rotator.selected)

with requests.get(
    "<endpoint>",
    *args,
    proxies={rotator.selected.scheme: rotator.selected.peername}
    **kwargs
) as response:
    ...
```

For more information, see available docstrings.
