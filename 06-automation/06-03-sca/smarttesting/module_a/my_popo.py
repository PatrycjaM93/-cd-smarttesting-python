from typing import Optional


class MyPopo:
    """
    Plain-Old Python object + gettery/settery. Niespotykane w Pythonie, raczej uważane
    za antypattern (tj. nie ma narzędzi korzystającej z tej konwencji i kod pisany jest
    na próżno.

    Raczej będziemy zawsze bezpośrednio przypisywać wartości do pól, np:
    ```
    inst = MyPopo()
    inst.name = "Janusz"
    ```

    Gdy jest potrzeba customizacji tego zachowania lub wprowadzenia pól read-only,
    zawsze można użyć dekoratora @property. Zobacz przykład poniżej dla `_age`.
    """

    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._surname: Optional[str] = None
        self._age: int = 0

    def get_name(self) -> Optional[str]:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value

    def get_surname(self) -> Optional[str]:
        return self._surname

    def set_surname(self, value: str) -> None:
        self._surname = value

    @property
    def age(self) -> int:
        """Gdybyśmy nie zrobili settera (poniżej) to mielibyśmy pole read-only.

        Oczywiście dopóki ktoś nie postanowi zrobić `inst._age = -10000` (:
        """
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0:
            raise ValueError("No bez jaj, ujemny wiek?!")

        self._age = value
