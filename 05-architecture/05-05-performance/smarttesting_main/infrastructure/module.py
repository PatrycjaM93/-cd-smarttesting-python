import injector
from sqlalchemy.orm import Session

from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting_main.infrastructure.verification_repo import (
    SqlAlchemyVerificationRepository,
)


class InfrastructureModule(injector.Module):
    @injector.provider
    def repo(self, session: Session) -> VerificationRepository:
        return SqlAlchemyVerificationRepository(session)
