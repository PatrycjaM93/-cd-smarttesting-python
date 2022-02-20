from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.income.monthly_income_client import MonthlyIncomeClient
from smarttesting.bik.score.income.monthly_income_score_evaluation import (
    MonthlyIncomeScoreEvaluation,
)
from tests.bik.score.utils import an_id


class TestMonthlyIncomeScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._client = Mock(spec_set=MonthlyIncomeClient)
        self._score_evaluation = MonthlyIncomeScoreEvaluation(self._client)

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi - obsługa minusowej wartości dochodów nie została dodana "
            "Brakuje implementacji dla przedziału 3501 - 5500 -> 30"
        )
    )
    @pytest.mark.parametrize(
        "monthly_income, points",
        [
            (Decimal("-1"), 0),
            (Decimal("0"), 0),
            (Decimal("1"), 0),
            (Decimal("200"), 0),
            (Decimal("500"), 0),
            (Decimal("501"), 10),
            (Decimal("502"), 10),
            (Decimal("1500"), 10),
            (Decimal("1501"), 20),
            (Decimal("1504"), 20),
            (Decimal("3500"), 20),
            (Decimal("3501"), 30),
            (Decimal("3600"), 30),
            (Decimal("5500"), 30),
            (Decimal("5501"), 40),
            (Decimal("5502"), 40),
            (Decimal("8888"), 40),
            (Decimal("10000"), 40),
            (Decimal("10001"), 50),
            (Decimal("10002"), 50),
            (Decimal("1000000"), 50),
        ],
    )
    def test_calculates_score_based_on_monthly_income(
        self, monthly_income: Decimal, points: int
    ) -> None:
        self._client.get_monthly_income = Mock(return_value=monthly_income)

        score = self._score_evaluation.evaluate(an_id())

        assert score.points == points

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa nulli nie została zaimplementowana")
    )
    def test_returns_0_when_monthly_income_none(self) -> None:
        self._client.get_monthly_income = Mock(return_value=None)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()
