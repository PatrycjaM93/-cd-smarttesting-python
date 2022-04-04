from typing import Optional


class MyPopo:
    """
    Odchudzone POPO - pola publiczne z domyślnymi wartościami.

    Bardziej pythonowe niż akcesory ale w 2020 roku i tak
    lepiej użyć @dataclass/@attr.s lub podobnej biblioteki.
    """

    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.surname: Optional[str] = None
        self.age: int = 0
