from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch


def test_should_find_any_empty_name():
    """W tym teście mockujemy wszystko co się da. Włącznie z mockowaniem listy.

    Mockujemy nawet metodę __len__ z klasy str by taki zmockowany string był uznany
    za "pusty".

    Nie przestrzegamy też podstawowej zasady higieny pracy z mockami - tj. używania
    `spec` lub `spec_set`.
    """
    name_mock = Mock(__len__=Mock(return_value=0))
    names_mock = Mock(__next__=Mock(side_effect=[name_mock, StopIteration]))
    names_mock.__iter__ = Mock(return_value=names_mock)

    with patch.object(Dao, "store_in_db"):
        assert _03_FraudService().any_name_is_empty(names_mock) is True


def test_should_find_any_empty_name_fixed():
    """Poprawiona wersja testu powyżej.

    Nie mockujemy listy - tworzymy ją.
    Nie patchujemy też klasy używanej bezpośrednio. Raczej powinniśmy zmienić
    design `_03_FraudService` by umożliwiała wstrzykiwanie zależności przez __init__,
    jeżeli testowanie jej bez `Dao` jest pożądane.
    """
    names = ["non empty", ""]

    assert _03_FraudService().any_name_is_empty(names) is True


def test_does_some_work_in_database_when_empty_string_found():
    """Przykład lepszego testu bez monkey-patching zbudowanego w oparciu o DI."""
    dao_mock = Mock(spec_set=Dao)
    names = ["non empty", ""]

    FraudServiceFixed(dao_mock).any_name_is_empty(names)

    dao_mock.store_in_db.assert_called_once()


class _03_FraudService:  # pylint: disable=invalid-name
    """Klasa, w której korzystamy bezpośrednio z innych obiektów."""

    def any_name_is_empty(self, names: List[str]) -> bool:
        for name in names:
            if not name:
                Dao.store_in_db()
                return True
        return False


class Dao:
    @classmethod
    def store_in_db(cls) -> None:
        pass


@dataclass
class FraudServiceFixed:
    _dao: Dao

    def any_name_is_empty(self, names: List[str]) -> bool:
        for name in names:
            if not name:
                self._dao.store_in_db()
                return True
        return False
