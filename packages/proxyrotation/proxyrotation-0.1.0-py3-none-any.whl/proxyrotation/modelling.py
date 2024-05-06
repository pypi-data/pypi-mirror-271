import enum
from dataclasses import dataclass, field


class Anonymity(str, enum.Enum):
    """The enum for proxy anonimity"""

    high = "elite proxy"
    medium = "anonymous"
    weak = "transparent"
    unknown = "unknown"

    @classmethod
    def from_string(cls, value: str) -> "Anonymity":
        try:
            return cls(value)
        except ValueError:
            return Anonymity.unknown


@dataclass(frozen=True, slots=True)
class Proxy:
    """proxy address object

    Attributes:
        host: The proxy IPv4 host address
        port: The proxy port number
        countrycode: The proxy ISO 3166-1 alpha-2 country code
        anonymity: The proxy anonymity level
        secure: If supports HTTPS or not
    """

    host: str = field(hash=True)
    port: int = field(hash=True)
    countrycode: str = field(hash=False)
    anonymity: Anonymity = field(hash=False)
    secure: bool = field(hash=False)

    @property
    def peername(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def protocol(self) -> str:
        return "HTTPS" if self.secure else "HTTP"

    @property
    def scheme(self) -> str:
        return self.protocol.lower()
