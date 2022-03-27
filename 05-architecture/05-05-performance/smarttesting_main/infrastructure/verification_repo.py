from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from smarttesting.verifier.customer.customer_verification_result import Status
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person_dto import VerifiedPersonDto
from smarttesting_main.infrastructure.verified_person import VerifiedPerson


@dataclass
class SqlAlchemyVerificationRepository(VerificationRepository):
    _session: Session

    def find_by_user_id(self, user_id: UUID) -> Optional[VerifiedPersonDto]:
        model = (
            self._session.query(VerifiedPerson)
            .filter(VerifiedPerson.uuid == str(user_id))
            .first()
        )
        if model:
            return VerifiedPersonDto(
                uuid=UUID(model.uuid),
                national_identification_number=model.national_identification_number,
                status=Status(model.status),
            )
        return None

    def save(self, verified_person: VerifiedPersonDto) -> None:
        model = VerifiedPerson(
            uuid=str(verified_person.uuid),
            national_identification_number=verified_person.national_identification_number,
            status=verified_person.status.value,
        )
        self._session.add(model)
        self._session.flush()
