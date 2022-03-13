import logging

from injector import Inject
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def fraud_detected_handler(
    repo: Inject[VerificationRepository],
    session: Inject[Session],
    *,
    customer_verification: CustomerVerification
) -> None:
    """Implementacja zadania przechodzącego przez brokera RabbitMQ."""
    logger.info("Got customer verification: %s", customer_verification)
    person = customer_verification.person
    result = customer_verification.result
    repo.save(
        VerifiedPerson(
            uuid=str(result.user_id),
            national_identification_number=person.national_id_number,
            status=result.status.name,
        )
    )
    session.commit()
    session.close()
