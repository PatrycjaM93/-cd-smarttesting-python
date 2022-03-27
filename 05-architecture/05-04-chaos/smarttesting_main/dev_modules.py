import injector
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)


class DevModule(injector.Module):
    """Moduł injectora nadpisujący niektóre klasy na potrzeby lokalnego środowiska."""

    @injector.provider
    def stubbed_bik_verification_service(self) -> BIKVerificationService:
        class BIKVerificationServiceStub(BIKVerificationService):
            def verify(self, customer: Customer) -> CustomerVerificationResult:
                if customer.person.surname == "Fraudeusz":
                    return CustomerVerificationResult.create_failed(customer.uuid)
                else:
                    return CustomerVerificationResult.create_passed(customer.uuid)

        return BIKVerificationServiceStub(_bik_service_url="")
