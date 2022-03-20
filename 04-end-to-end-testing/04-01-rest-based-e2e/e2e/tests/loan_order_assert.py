from dataclasses import dataclass

from e2e.smarttesting.order.loan_order import LoanOrder, Status


@dataclass
class LoanOrderAssert:
    _loan_order: LoanOrder

    def customer_verification_passed(self) -> None:
        assert self._loan_order.status == Status.VERIFIED

    def customer_verification_failed(self) -> None:
        assert self._loan_order.status == Status.REJECTED
