import ipaddress
import typing

from bs4 import BeautifulSoup as BS

from proxyrotation.modelling import Anonymity, Proxy


try:
    import aiohttp
    import aiostream

    has_async = True
except ImportError:
    has_async = False


def is_ipv4_address(address: typing.Union[str, Proxy]) -> bool:
    """If a proxy address conforms to a IPv4 address"""
    if isinstance(address, Proxy):
        address = address.host

    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


def batch_response_parsing(response: str) -> set[Proxy]:
    """parses batch of proxy addresses from a raw HTML response"""
    soup = BS(response, "html.parser")

    candidateset = zip(
        map(lambda x: x.text.lower(), soup.findAll("td")[::8]),
        map(lambda x: x.text.lower(), soup.findAll("td")[1::8]),
        map(lambda x: x.text.upper(), soup.findAll("td")[2::8]),
        map(lambda x: x.text.lower(), soup.findAll("td")[4::8]),
        map(lambda x: x.text.lower(), soup.findAll("td")[6::8]),
    )

    available = set()

    for host, port, countrycode, anonymity, secure in candidateset:
        if not is_ipv4_address(host):
            continue

        available.add(
            Proxy(
                host=host,
                port=int(port),
                countrycode=countrycode,
                anonymity=Anonymity.from_string(anonymity),
                secure=secure == "yes",
            )
        )

    return available
