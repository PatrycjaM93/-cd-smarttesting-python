import injector
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting_main.infrastructure.verification_repo import (
    SqlAlchemyVerificationRepository,
)
from sqlalchemy.orm import Session


class InfrastructureModule(injector.Module):
    @injector.provider
    def repo(self, session: Session) -> VerificationRepository:
        return SqlAlchemyVerificationRepository(session)
