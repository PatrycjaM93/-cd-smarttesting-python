from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from loan_orders.customer.person import Person


@dataclass
class Customer:
    """Klient. Klasa opakowująca osobę do zweryfikowania."""

    _uuid: UUID
    _person: Person
    id: Optional[str] = None

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
