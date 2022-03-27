import enum
from dataclasses import dataclass
from uuid import UUID


class Status(enum.Enum):
    VERIFICATION_PASSED = "VERIFICATION_PASSED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"


@dataclass(frozen=True)
class CustomerVerificationResult:
    """Rezultat weryfikacji klienta."""

    _user_id: UUID
    _status: Status

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def status(self) -> Status:
        return self._status

    @property
    def passed(self) -> bool:
        return self._status == Status.VERIFICATION_PASSED

    @staticmethod
    def create_passed(user_id: UUID) -> "CustomerVerificationResult":
        return CustomerVerificationResult(user_id, Status.VERIFICATION_PASSED)

    @staticmethod
    def create_failed(user_id: UUID) -> "CustomerVerificationResult":
        return CustomerVerificationResult(user_id, Status.VERIFICATION_FAILED)
