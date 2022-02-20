from datetime import date
from decimal import Decimal

from smarttesting.customer.customer import Customer
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.loan_order import LoanOrder
from smarttesting.order.promotion import Promotion


class LoanOrderService:
    """Serwis procesujący przynawanie pożyczek.

    Działa w zależności od typu pożyczki i obowiązujących promocji.
    """

    def student_loan_order(self, customer: Customer) -> LoanOrder:
        if not customer.is_student:
            raise ValueError(f"Cannot order student loan, {customer} is not a student.")

        today = date.today()
        loan_order = LoanOrder(today, customer)
        loan_order.type = LoanType.STUDENT
        loan_order.promotions.append(Promotion("Student Promo", Decimal("10")))
        loan_order.commission = Decimal("200")
        return loan_order
