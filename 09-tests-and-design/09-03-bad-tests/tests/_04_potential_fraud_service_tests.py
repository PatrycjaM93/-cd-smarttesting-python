"""Moduł z testami pokazująca jak stanowość może pokrzyżować nam plany w powtarzalnych
wynikach testów.

Najpierw zakomentuj `@pytest.mark.skip` żeby wszystkie testy się uruchomiły.

Następnie uruchom testy kilkukrotnie - zobaczysz, że czasami przechodzą, a czasami nie.
W czym problem?
"""
from dataclasses import dataclass
from typing import Dict, Optional

import pytest

pytest_plugins = ["pytest-randomly"]


@pytest.mark.skip
def test_counts_potential_frauds() -> None:
    """Test ten oczekuje, że zawsze uruchomi się pierwszy.

    Dlatego oczekuje, że w cache'u będzie jeden wynik. Dla przypomnienia, cache jest
    współdzielony przez wszystkie testy, ponieważ jest statyczny.

    W momencie uruchomienia testów w innej kolejności, inne testy też dodają wpisy
    do cache'a. Zatem nie ma możliwości, żeby rozmiar cache'a wynosił 1.
    """
    cache = PotentialFraudCache()
    service = PotentialFraudService(cache)

    service.set_fraud("Kowalski")

    assert len(cache) == 1


def test_sets_potential_fraud() -> None:
    """Przykład testu, który weryfikuje czy udało nam się dodać wpis do cache'a.

    Zwiększa rozmiar cache'a o 1. Gdy ten test zostanie uruchomiony przed
    `test_counts_potential_frauds` - wspomniany test się wywali.
    """
    cache = PotentialFraudCache()
    service = PotentialFraudService(cache)

    service.set_fraud("Oszustowski")

    assert cache.fraud("Oszustowski") is not None


def test_stores_potential_fraud() -> None:
    """
    Potencjalne rozwiązanie problemu wspóldzielonego stanu.

    Najpierw zapisujemy stan wejściowy - jaki był rozmiar cache'a.
    Dodajemy wpis do cache'a i sprawdzamy czy udało się go dodać i czy rozmiar jest
    większy niż był.

    W przypadku uruchomienia wielu testów równolegle, sam fakt weryfikacji rozmiaru
    jest niedostateczny, gdyż inny test mógł zwiększyć rozmiar cache'a. Koniecznym
    jest zweryfikowanie, że istnieje w cache'u wpis dot. Kradzieja.

    BONUS: Jeśli inny test weryfikował usunięcie wpisu z cache'a, to asercja na rozmiar
    może nam się wysypać. Należy rozważyć, czy nie jest wystarczającym zweryfikowanie
    tylko obecności Kradzieja w cache'u!
    """
    cache = PotentialFraudCache()
    service = PotentialFraudService(cache)
    initial_size = len(cache)

    service.set_fraud("Kradziej")

    assert len(cache) > initial_size
    assert cache.fraud("Kradziej") is not None


@dataclass(frozen=True)
class PotentialFraud:
    """Struktura reprezentująca potencjalnego oszusta."""

    name: str


class PotentialFraudCache:
    """Stan współdzielony między instancjami. Problemy? Np. nie zapewnimy wyłączności
    dla pojedynczego wątku i dopuścimy odczyt/modyfikację danych przez wiele wątków
    naraz.

    Przykładem może być aplikacja webowa z workerami-wątkami.
    """

    _cache: Dict[str, PotentialFraud] = {}

    def fraud(self, name: str) -> Optional[PotentialFraud]:
        return self._cache.get(name)

    def put(self, fraud: PotentialFraud) -> None:
        self._cache[fraud.name] = fraud

    def __len__(self) -> int:
        return len(self._cache)


@dataclass
class PotentialFraudService:
    """Serwis aplikacyjny opakowujący wywołania do cache'a."""

    _cache: PotentialFraudCache

    def set_fraud(self, name: str) -> None:
        self._cache.put(PotentialFraud(name))
