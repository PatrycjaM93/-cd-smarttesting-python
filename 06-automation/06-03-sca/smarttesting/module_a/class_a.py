from smarttesting.module_b.class_b import ClassB
from smarttesting.module_c.class_c import ClassC


class ClassA:
    """
    Odpowiednik kodu ze slajdów do wizualizacji wzajemnej zależności modułów.

    Klasa ClassA z modułu A korzysta z modułów B i C.
    """

    def __init__(self, class_b: ClassB, class_c: ClassC) -> None:
        self.class_b = class_b
        self.class_c = class_c
