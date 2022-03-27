import abc
from typing import Optional
from uuid import UUID

from smarttesting.verifier.customer.verified_person_dto import VerifiedPersonDto


class VerificationRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Optional[VerifiedPersonDto]:
        pass

    @abc.abstractmethod
    def save(self, verified_person: VerifiedPersonDto) -> None:
        pass
