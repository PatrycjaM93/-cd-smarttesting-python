from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from smarttesting.db.mongo_db_accessor import MongoDbAccessor
from smarttesting.db.postgres_accessor import PostgresAccessor
from smarttesting.event.event_emitter import EventEmitter
from smarttesting.loan.loan import Loan
from smarttesting.loan.loan_created_event import LoanCreatedEvent
from smarttesting.loan.validation.commission_validation_exception import (
    CommissionValidationException,
)
from smarttesting.loan.validation.number_of_installments_validation_exception import (
    NumberOfInstallmentsValidationException,
)
from smarttesting.order.loan_order import LoanOrder


@dataclass(unsafe_hash=True)
class LoanService:
    _event_emitter: EventEmitter
    _mongo_db_accessor: MongoDbAccessor
    _postgres_accessor: PostgresAccessor

    def create_loan(self, loan_order: LoanOrder, number_of_installments: int) -> Loan:
        # Forget to pass argument (validate field instead)
        self._validate_number_of_installments(number_of_installments)
        # Forget to add this method add first
        assert loan_order.commission is not None
        self._validate_commission(loan_order.commission)
        self.update_promotions(loan_order)
        loan = Loan(date.today(), loan_order, number_of_installments)
        self._event_emitter.emit(LoanCreatedEvent(loan.uuid))
        return loan

    def _validate_commission(self, commission: Decimal) -> None:
        if commission <= self._mongo_db_accessor.get_min_commission():
            raise CommissionValidationException()

    def _validate_number_of_installments(self, number_of_installments: int) -> None:
        if number_of_installments <= 0:
            raise NumberOfInstallmentsValidationException()

    def update_promotions(self, loan_order: LoanOrder) -> None:
        """Visible for tests.

        Potencjalny kandydat na osobną klasę.
        """
        valid_promotions = set(
            self._postgres_accessor.get_valid_promotions_for_date(date.today())
        )
        loan_order_promotions = set(loan_order.promotions)
        loan_order.promotions = list(
            valid_promotions.intersection(loan_order_promotions)
        )
