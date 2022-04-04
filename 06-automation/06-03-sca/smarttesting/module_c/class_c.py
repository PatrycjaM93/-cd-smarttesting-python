import typing

if typing.TYPE_CHECKING:
    # importy cyklicznie nie będa działać w Pythonie,
    # jednak da się je ogarnąc na potrzeby TYPE_CHECKINGU
    from smarttesting.module_a.class_a import ClassA
    from smarttesting.module_b.class_b import ClassB


class ClassC:
    """
    Odpowiednik kodu ze slajdów do wizualizacji wzajemnej zależności modułów.

    Klasa ClassC z modułu C korzysta z modułów A i B.
    """

    def __init__(self, class_a: ClassA, class_b: ClassB) -> None:
        self.class_a = class_a
        self.class_b = class_b
