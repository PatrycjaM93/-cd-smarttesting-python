from dataclasses import dataclass


@dataclass(frozen=True)
class Client:
    name: str
    has_debt: bool
