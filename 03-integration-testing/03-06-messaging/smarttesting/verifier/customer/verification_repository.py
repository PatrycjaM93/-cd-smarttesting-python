import abc
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from smarttesting.verifier.customer.verified_person import VerifiedPerson
from sqlalchemy.orm import Session


class VerificationRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Optional[VerifiedPerson]:
        pass

    @abc.abstractmethod
    def save(self, verified_person: VerifiedPerson) -> None:
        pass


@dataclass
class SqlAlchemyVerificationRepository(VerificationRepository):
    _session: Session

    def find_by_user_id(self, user_id: UUID) -> Optional[VerifiedPerson]:
        return (
            self._session.query(VerifiedPerson)
            .filter(VerifiedPerson.uuid == str(user_id))
            .first()
        )

    def save(self, verified_person: VerifiedPerson) -> None:
        self._session.add(verified_person)
        self._session.flush()
