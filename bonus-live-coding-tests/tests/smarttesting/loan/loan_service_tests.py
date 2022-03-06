from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from smarttesting.db.mongo_db_accessor import MongoDbAccessor
from smarttesting.db.postgres_accessor import PostgresAccessor
from smarttesting.event.event_emitter import EventEmitter
from smarttesting.loan.loan_service import LoanService
from smarttesting.loan.validation.commission_validation_exception import (
    CommissionValidationException,
)
from smarttesting.order.promotion import Promotion
from tests.smarttesting.loan.factories import build_loan_order


class TestLoanService:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._event_emitter = EventEmitter()
        self._mongo_db_accessor = Mock(
            spec_set=MongoDbAccessor,
            get_min_commission=Mock(return_value=Decimal("200")),
        )
        postgres_accessor = StubPostgresAccessor()
        self._loan_service = LoanService(
            self._event_emitter,
            self._mongo_db_accessor,
            postgres_accessor,
        )

    def test_crates_loan(self) -> None:
        loan_order = build_loan_order()

        loan = self._loan_service.create_loan(loan_order, number_of_installments=3)

        assert loan.uuid is not None

    def test_emits_event_when_loan_created(self) -> None:
        loan_order = build_loan_order()

        with patch.object(
            self._event_emitter, "emit", wraps=self._event_emitter.emit
        ) as emit_captor:
            self._loan_service.create_loan(loan_order, number_of_installments=3)

        assert len(emit_captor.mock_calls) == 1
        event_called_with = emit_captor.mock_calls[0].args[0]
        assert event_called_with.uuid is not None

    @pytest.mark.parametrize(
        "commission", [Decimal("0"), Decimal("-1"), Decimal("199")]
    )
    def test_raises_exception_when_commission_is_incorrect(
        self, commission: Decimal
    ) -> None:
        loan_order = build_loan_order(
            amount=Decimal("2000"), interest_rate=Decimal("5"), commission=commission
        )

        with pytest.raises(CommissionValidationException):
            self._loan_service.create_loan(loan_order, number_of_installments=5)

    def test_doesnt_raise_exception_when_there_is_no_promotion(self) -> None:
        loan_order = build_loan_order(promotions=[])

        try:
            self._loan_service.create_loan(loan_order, number_of_installments=6)
        except Exception:  # pylint: disable=broad-except
            pytest.fail("Should not raise any exception!")

    def test_removes_invalid_promotions(self) -> None:
        loan_order = build_loan_order(
            promotions=[Promotion("Promo not in DB", Decimal("55"))]
        )

        self._loan_service.update_promotions(loan_order)

        assert loan_order.promotions == []


class StubPostgresAccessor(PostgresAccessor):
    def update_promotion_statistics(self, promotion_name: str) -> None:
        pass  # do nothing

    def update_promotion_discount(
        self, promotion_name: str, new_discount: Decimal
    ) -> None:
        pass  # do nothing

    def get_valid_promotions_for_date(self, a_date: date) -> list[Promotion]:
        return [
            Promotion("test 10", Decimal("10")),
            Promotion("test 20", Decimal("20")),
        ]
