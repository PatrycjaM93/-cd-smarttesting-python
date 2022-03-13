from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)


class ExceptionThrowingBikService(BIKVerificationService):
    def __init__(self) -> None:
        super().__init__("")

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        raise ValueError("You shouldn't be calling that!")
