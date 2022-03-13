import copy
from typing import Dict, Optional, TypeVar
from uuid import UUID

from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson

ToCopy = TypeVar("ToCopy")


class InMemoryVerificationRepository(VerificationRepository):
    """Abstrakcja nad zwykłą mapę symulującą bazę danych."""

    def __init__(self) -> None:
        self._storage: Dict[UUID, VerifiedPerson] = {}

    def find_by_user_id(self, user_id: UUID) -> Optional[VerifiedPerson]:
        return self._copy(self._storage.get(user_id))

    def save(self, verified_person: VerifiedPerson) -> None:
        self._storage[UUID(verified_person.uuid)] = self._copy(verified_person)

    @staticmethod
    def _copy(arg: ToCopy) -> ToCopy:
        """Kopiowanie jest pomocne aby ustrzec się przed niechcianymi efektami.

        Obiekty w Pythonie przekazywane są przez referencję, zatem jeżeli będziemy
        operować na obiekcie wyciągniętym z repo, wprowadzimy i jakieś zmiany,
        zapomnimy zapisać rezultatu i NIE kopiujemy obiektów, to w repo będzie
        nadal zmieniona wersja, co może prowadzić do false-positive'ów i rozjazdu
        między testami, a produkcją."""
        return copy.deepcopy(arg)
