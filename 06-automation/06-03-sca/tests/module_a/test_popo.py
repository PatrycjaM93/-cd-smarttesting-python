from smarttesting.module_a.my_popo import MyPopo


def test_setters_and_getters():
    """Test pokazujący testowanie getterów i setterów.

    Jeśli w tych metodach nie ma specjalnej logiki najlepiej nie pisać takich testów.
    Coverage i tak będzie zapewniony dzięki testom wyżej-poziomowym klas/funkcji, które
    używają tej struktury danych.
    """
    popo = MyPopo()
    popo.set_name("Name")
    popo.set_surname("Surname")
    popo.age = 10

    assert popo.get_name() == "Name"
    assert popo.get_surname() == "Surname"
    assert popo.age == 10
