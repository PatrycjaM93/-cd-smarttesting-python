"""Źle nazwane testy chociaż klasa i plik sa nazwane poprawnie.

Nazwa funkcji/metody testowej powinna zaczynać się słowem test_
"""


class TestDummy:
    def tst_passing(self) -> None:
        assert True


def should_pass() -> None:
    assert True
