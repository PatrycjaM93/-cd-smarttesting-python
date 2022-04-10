from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Promotion:
    """Reprezentuje promocję dla oferty pożyczek."""

    name: str
    discount: Decimal
