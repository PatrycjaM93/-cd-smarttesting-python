from unittest.mock import patch

from smarttesting import tasks
from smarttesting.models import Person
from smarttesting.taxes import TaxService


class Test01BadClass:
    """Klasa z przykładami źle zaprojektowanego kodu.

    Sam kod w sobie niewiele robi, chodzi jedynie o zaprezentowanie koncepcji
    i często powielanych w Pythonie zachowań utrudniających potem testowanie.

    Czy zdarzyło Ci się, że dodawanie kolejnych testów było dla Ciebie drogą przez
    mękę?

    Czy znasz przypadki, gdzie potrzebne były setki linijek kodu przygotowującego pod
    uruchomienie testu? Oznacza to, że najprawdopodobniej albo nasz sposób testowania
    jest niepoprawny albo architektura aplikacji jest zła.
    """

    def test_heavy_monkey_patching(self) -> None:
        """Patchowanie jest zaskakująco chętnie wykorzystywaną techniką w testowaniu
        w Pythonie, jednak z punktu widzenia inżynierii oprogramowania jest to praktyka
        mocno wątpliwa.

        Tak naprawdę bardzo silnie cementuje nasz kod, będąc bardziej obejściem na
        problemy z ukrytymi wejściami i wyjściami do testowanego kodu.
        Ukryte wejścia/wyjścia to wszystko, czego testowana funkcja/metoda nie dostaje
        w argumencie lub przez self., ale co jest potrzebne do jej działania.

        Pokazywane w poprzednich lekcjach podejście wykorzystujące Dependency Injection
        z kontenerami IoC to sposób na pełną kontrolę tych kłopotliwych zależności.
        """
        person = Person(person_id=1, name="Jacek", surname="Kowalski")

        # Najpierw trzeba się grubo napracować patchując wszystkie lekkomyślnie
        # zaimplementowane zależności z różnych zakątków aplikacji...
        with patch.object(TaxService, "calculate") as tax_calculate_mock:
            tax_calculate_mock.return_value = 10
            # ...i modlić się, żeby nikt niczego nie przeniósł, bo patche od razu
            # przestaną działać
            with patch.object(tasks.send_email, "delay") as delay_mock:
                person.calculate()  # wołamy metodę której nazwa niewiele mówi

            tax_calculate_mock.assert_called_once()
            delay_mock.assert_called_once_with(person_id=person.person_id, dues=10)
