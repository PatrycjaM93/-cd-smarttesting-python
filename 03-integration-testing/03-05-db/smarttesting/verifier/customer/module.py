from typing import Set

import injector
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification_repository import (
    SqlAlchemyVerificationRepository,
    VerificationRepository,
)
from smarttesting.verifier.verification import Verification
from sqlalchemy.orm import Session


class CustomerModule(injector.Module):
    """Moduł injectora dla modułu klienta."""

    def __init__(self, bik_url: str = "http://example.org") -> None:
        self._bik_url = bik_url

    @injector.provider
    def bik_verification_service(self) -> BIKVerificationService:
        return BIKVerificationService(self._bik_url)

    @injector.provider
    def verification_repository(self, session: Session) -> VerificationRepository:
        return SqlAlchemyVerificationRepository(session)

    @injector.provider
    def customer_verifier(
        self,
        bik_service: BIKVerificationService,
        verifications: Set[Verification],
        repo: VerificationRepository,
    ) -> CustomerVerifier:
        return CustomerVerifier(bik_service, verifications, repo)
