import typing

from smarttesting.module_c.class_c import ClassC

if typing.TYPE_CHECKING:
    # importy cyklicznie nie będa działać w Pythonie
    from smarttesting.module_a.class_a import ClassA


class ClassB:
    """
    Odpowiednik kodu ze slajdów do wizualizacji wzajemnej zależności modułów.

    Klasa ClassB z modułu B korzysta z modułów A i C.
    """

    def __init__(self, class_a: ClassA, class_c: ClassC) -> None:
        self.class_a = class_a
        self.class_c = class_c
