import logging
from dataclasses import dataclass
from typing import Optional

from loan_orders.fraud import client as fraud_client
from loan_orders.order.loan_order import LoanOrder, Status
from loan_orders.repositories.loan_order_repository import LoanOrderRepository

logger = logging.getLogger(__name__)


@dataclass
class LoanOrderService:
    _repository: LoanOrderRepository

    def verify_loan_order(self, order: LoanOrder) -> str:
        customer = order.customer
        verification_result = fraud_client.verify_customer(customer)
        if not verification_result.passed:
            logger.warning("Customer %s has not passed verification", customer)
            order.status = Status.REJECTED
        else:
            order.status = Status.VERIFIED

        return self._repository.save(order)

    def find_order(self, order_id: str) -> Optional[LoanOrder]:
        return self._repository.get(order_id)
