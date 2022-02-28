from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from smarttesting.customer.customer import Customer
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.promotion import Promotion


@dataclass
class LoanOrder:

    _order_date: date
    customer: Customer
    type: Optional[LoanType] = None
    amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    promotions: List[Promotion] = field(default_factory=list)

    @property
    def order_date(self) -> date:
        return self._order_date

    def add_manager_discount(self, manager_uuid: UUID) -> None:
        new_promo = Promotion(f"Manager Promo: {manager_uuid}", Decimal("50"))
        self.promotions.append(new_promo)
