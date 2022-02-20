from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True)
class Pesel:
    _pesel: str

    def __init__(self, pesel: str) -> None:
        if len(pesel) != 11:
            raise ValueError("PESEL must be of 11 chars")
        self._pesel = pesel

    @property
    def pesel(self) -> str:
        return self._pesel

    @property
    def obfuscated(self) -> str:
        return self._pesel[7:]

    def __str__(self) -> str:
        return self.obfuscated

    __repr__ = __str__
