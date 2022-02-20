from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.bik.score.credit.credit_info import CreditInfo, DebtPaymentHistory
from smarttesting.bik.score.credit.credit_info_repository import CreditInfoRepository
from smarttesting.bik.score.credit.credit_info_score_evaluation import (
    CreditInfoScoreEvaluation,
)
from smarttesting.bik.score.domain.score import Score
from tests.bik.score.utils import an_id


class TestCreditInfoScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._repository = Mock(spec_set=CreditInfoRepository)
        self._score_evaluation = CreditInfoScoreEvaluation(self._repository)

    def test_returns_0_for_none_credit_info(self) -> None:
        self._repository.find_credit_info = Mock(return_value=None)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason="Test nie przechodzi; obsługa None'ów nie została zaimplementowana"
    )
    def test_returns_0_for_none_fields_of_credit_info(self) -> None:
        credit_info = CreditInfo(None, None, None)
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi "
            "przedział powyżej 10000 nie został zaimplementowany "
            "obsługa niepoprawnej wartości -1 nie została zaimplementowana"
        )
    )
    @pytest.mark.parametrize(
        "living_cost, points",
        [
            (Decimal("20000"), 0),
            (Decimal("10001"), 0),
            (Decimal("10000"), 0),
            (Decimal("8000"), 0),
            (Decimal("6550"), 0),
            (Decimal("6501"), 0),
            (Decimal("6500"), 10),
            (Decimal("6499"), 10),
            (Decimal("5000"), 10),
            (Decimal("4502"), 10),
            (Decimal("4501"), 10),
            (Decimal("4500"), 20),
            (Decimal("4499"), 20),
            (Decimal("3000"), 20),
            (Decimal("2502"), 20),
            (Decimal("2501"), 20),
            (Decimal("2500"), 40),
            (Decimal("2499"), 40),
            (Decimal("2000"), 40),
            (Decimal("1001"), 40),
            (Decimal("1000"), 40),
            (Decimal("999"), 50),
            (Decimal("1"), 50),
            (Decimal("0"), 50),
            (Decimal("-1"), 0),
        ],
    )
    def test_evaluates_score_based_on_current_living_costs(
        self, living_cost: Decimal, points: int
    ) -> None:
        credit_info = CreditInfo(
            Decimal("5501"),
            living_cost,
            DebtPaymentHistory.NOT_A_SINGLE_PAID_INSTALLMENT,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score.points == points

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi "
            "przedział powyżej 10000 nie został zaimplementowany "
            "obsługa niepoprawnej wartości -1 nie została zaimplementowana"
        )
    )
    @pytest.mark.parametrize(
        "current_debt, points",
        [
            (Decimal("-1"), 0),
            (Decimal("20000"), 0),
            (Decimal("10001"), 0),
            (Decimal("10000"), 0),
            (Decimal("8000"), 0),
            (Decimal("5550"), 0),
            (Decimal("5501"), 0),
            (Decimal("5500"), 10),
            (Decimal("5499"), 10),
            (Decimal("4000"), 10),
            (Decimal("3502"), 10),
            (Decimal("3501"), 10),
            (Decimal("3500"), 20),
            (Decimal("3499"), 20),
            (Decimal("2000"), 20),
            (Decimal("1502"), 20),
            (Decimal("1501"), 20),
            (Decimal("1500"), 40),
            (Decimal("1499"), 40),
            (Decimal("1000"), 40),
            (Decimal("501"), 40),
            (Decimal("500"), 40),
            (Decimal("499"), 50),
            (Decimal("200"), 50),
            (Decimal("1"), 50),
            (Decimal("0"), 50),
        ],
    )
    def test_evaluates_score_based_on_current_debt(
        self, current_debt: Decimal, points: int
    ) -> None:
        credit_info = CreditInfo(
            current_debt,
            Decimal("6501"),
            DebtPaymentHistory.NOT_A_SINGLE_PAID_INSTALLMENT,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score.points == points

    def test_evaluates_score_for_not_paying_customer(self) -> None:
        credit_info = CreditInfo(
            Decimal("5501"),
            Decimal("6501"),
            DebtPaymentHistory.NOT_A_SINGLE_PAID_INSTALLMENT,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    def test_evaluates_score_for_always_paying_customer(self) -> None:
        credit_info = CreditInfo(
            Decimal("5501"),
            Decimal("6501"),
            DebtPaymentHistory.NOT_A_SINGLE_UNPAID_INSTALLMENT,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(50)

    def test_evaluates_score_for_often_missing_payment_customer(self) -> None:
        credit_info = CreditInfo(
            Decimal("5501"),
            Decimal("6501"),
            DebtPaymentHistory.MULTIPLE_UNPAID_INSTALLMENTS,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(10)

    def test_evaluates_score_for_rarely_missing_payment_customer(self) -> None:
        credit_info = CreditInfo(
            Decimal("5501"),
            Decimal("6501"),
            DebtPaymentHistory.INDIVIDUAL_UNPAID_INSTALLMENTS,
        )
        self._repository.find_credit_info = Mock(return_value=credit_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(30)
