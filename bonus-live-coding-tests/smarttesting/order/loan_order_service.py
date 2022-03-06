from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from smarttesting.customer.customer import Customer
from smarttesting.db.mongo_db_accessor import MongoDbAccessor
from smarttesting.db.postgres_accessor import PostgresAccessor
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.loan_order import LoanOrder
from smarttesting.order.promotion import Promotion


@dataclass(unsafe_hash=True)
class LoanOrderService:
    _postgres_accessor: PostgresAccessor
    _mongo_db_accessor: MongoDbAccessor

    """Serwis procesujący przynawanie pożyczek.

     Działa w zależności od typu pożyczki i obowiązujących promocji."""

    def student_loan_order(self, customer: Customer) -> LoanOrder:
        if not customer.student:
            raise ValueError("Cannot order student loan if customer is not a student.")

        today = date.today()
        loan_order = LoanOrder(
            today,
            customer,
            LoanType.STUDENT,
            Decimal("2000"),
            Decimal("5"),
            Decimal("200"),
        )
        discount = self._mongo_db_accessor.get_promotion_discount("Student Promo")
        loan_order.promotions.append(Promotion("Student Promo", discount))
        self._postgres_accessor.update_promotion_statistics("Student Promo")
        return loan_order
