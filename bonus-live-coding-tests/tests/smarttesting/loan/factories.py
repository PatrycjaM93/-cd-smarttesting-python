from datetime import date
from decimal import Decimal
from uuid import uuid4

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.order.loan_order import LoanOrder
from smarttesting.order.promotion import Promotion


def build_loan_order(
    amount: Decimal = Decimal("2000"),
    interest_rate: Decimal = Decimal("5"),
    commission: Decimal = Decimal("300"),
    promotions: list[Promotion] | None = None,
) -> LoanOrder:
    if promotions is None:
        promotions = []

    person = Person(
        "Maria", "Kowalska", date(1989, 3, 10), Gender.FEMALE, "89031013409"
    )
    customer = Customer(uuid4(), person)
    loan_order = LoanOrder(
        date.today(),
        customer=customer,
        amount=amount,
        interest_rate=interest_rate,
        commission=commission,
    )
    loan_order.promotions.extend(promotions)
    return loan_order
