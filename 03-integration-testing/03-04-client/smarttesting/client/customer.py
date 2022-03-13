from dataclasses import dataclass
from uuid import UUID

from smarttesting.client.person import Person


@dataclass
class Customer:
    """Klient. Klasa opakowująca osobę do zweryfikowania."""

    _uuid: UUID
    _person: Person

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def person(self) -> Person:
        return self._person

    @property
    def is_student(self) -> bool:
        return self._person.is_student

    @property
    def student(self):
        return self._person.student
