import abc
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from smarttesting.customer.customer import Customer
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.loan_order import LoanOrder
from smarttesting.order.promotion import Promotion


class PostgresDao(abc.ABC):
    @abc.abstractmethod
    def get_promotion_discount(self, promotion_name: str) -> Decimal:
        pass

    @abc.abstractmethod
    def update_promotion_statistics(self, promotion_name: str) -> None:
        pass

    @abc.abstractmethod
    def update_promotion_discount(
        self, promotion_name: str, new_discount: Decimal
    ) -> None:
        pass


class MongoDbDao:
    pass


@dataclass
class LoanOrderService:
    """Serwis procesujący przynawanie pożyczek.

    Działa w zależności od typu pożyczki i obowiązujących promocji.
    """

    _postgres_dao: PostgresDao
    _mongo_db_dao: MongoDbDao

    def student_loan_order(self, customer: Customer) -> LoanOrder:
        if not customer.is_student:
            raise ValueError(f"Cannot order student loan, {customer} is not a student.")

        today = date.today()
        loan_order = LoanOrder(today, customer)
        loan_order.type = LoanType.STUDENT
        discount = self._postgres_dao.get_promotion_discount("Student Promo")
        loan_order.promotions.append(Promotion("Student Promo", discount))
        loan_order.commission = Decimal("200")

        self._postgres_dao.update_promotion_statistics("Student Promo")

        return loan_order
