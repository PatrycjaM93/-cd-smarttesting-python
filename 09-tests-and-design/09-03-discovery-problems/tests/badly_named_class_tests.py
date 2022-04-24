class BadlyNamedClassWithTests:
    """Źle nazwana klasa uniemożliwiająca odkrycie jej przez pytesta.

    Przy obecnych ustawieniach, nazwa klasa powinna zaczynać się od słowa "Test".
    Testowa metoda jest poprawnie nazwana, jednak nie zostanie "odkryta".
    """

    def test_passing(self) -> None:
        assert True
