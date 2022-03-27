from dataclasses import dataclass
from uuid import UUID

from smarttesting.verifier.customer.customer_verification_result import Status


@dataclass
class VerifiedPersonDto:
    uuid: UUID
    national_identification_number: str
    status: Status
