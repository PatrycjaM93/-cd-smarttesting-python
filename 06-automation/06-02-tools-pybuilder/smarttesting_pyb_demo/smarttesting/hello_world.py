from typing import Protocol


class Writable(Protocol):
    def write(self, data: str) -> None:
        ...


def hello_world(out: Writable) -> None:
    out.write("Hello, world!\n")
