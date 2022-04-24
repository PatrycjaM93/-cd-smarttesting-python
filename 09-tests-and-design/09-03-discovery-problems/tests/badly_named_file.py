"""Dobrze nazwane klasy testowe i testy, jednak plik o takiej nazwie jest ignorowany."""


class TestDummy:
    def test_passing(self) -> None:
        assert True


def test_passes() -> None:
    assert True
