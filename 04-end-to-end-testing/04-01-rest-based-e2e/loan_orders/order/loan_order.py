from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from loan_orders.customer.customer import Customer
from loan_orders.order.promotion import Promotion


class Status(Enum):
    NEW = "NEW"
    VERIFIED = "VERIFIED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass
class LoanOrder:

    id: Optional[str]
    customer: Customer
    _uuid: UUID = field(default_factory=uuid4)
    _order_date: date = field(default_factory=date.today)
    amount: Optional[Decimal] = field(default=None, metadata={"as_string": True})
    interest_rate: Optional[Decimal] = field(default=None, metadata={"as_string": True})
    commission: Optional[Decimal] = field(default=None, metadata={"as_string": True})
    promotions: List[Promotion] = field(default_factory=list)
    status: Status = Status.NEW

    @property
    def uuid(self):
        return self._uuid

    @property
    def order_date(self) -> date:
        return self._order_date

    def add_manager_discount(self, manager_uuid: UUID) -> None:
        new_promo = Promotion(f"Manager Promo: {manager_uuid}", Decimal("50"))
        self.promotions.append(new_promo)
