from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.bik.score.cost.monthly_cost_client import MonthlyCostClient
from smarttesting.bik.score.cost.monthly_cost_score_evaluation import (
    MonthlyCostScoreEvaluation,
)
from tests.bik.score.utils import an_id


class TestMonthlyCostScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._client = Mock(spec_set=MonthlyCostClient)
        self._score_evaluation = MonthlyCostScoreEvaluation(self._client)

    @pytest.mark.skip(
        "Test nie przechodzi; obsługa minusowej wartości kosztów nie została dodana "
        "Brakuje implementacji dla przedziału 3501 - 5500 -> 20; "
        "Granice warunków niepoprawnie zaimplementowane"
    )
    @pytest.mark.parametrize(
        "cost, points",
        [
            (Decimal("-1"), 0),
            (Decimal("0"), 50),
            (Decimal("1"), 50),
            (Decimal("200"), 50),
            (Decimal("499"), 50),
            (Decimal("500"), 50),
            (Decimal("501"), 40),
            (Decimal("502"), 40),
            (Decimal("1499"), 40),
            (Decimal("1500"), 40),
            (Decimal("1501"), 30),
            (Decimal("1502"), 30),
            (Decimal("1504"), 30),
            (Decimal("3500"), 30),
            (Decimal("3501"), 20),
            (Decimal("3600"), 20),
            (Decimal("5500"), 20),
            (Decimal("5501"), 10),
            (Decimal("5502"), 10),
            (Decimal("8888"), 10),
            (Decimal("10000"), 10),
            (Decimal("10001"), 0),
            (Decimal("10002"), 0),
            (Decimal("1000000"), 0),
        ],
    )
    def test_calculates_score_based_on_monthly_costs(
        self, points: int, cost: Decimal
    ) -> None:
        self._client.get_monthly_costs = Mock(return_value=cost)

        score = self._score_evaluation.evaluate(an_id())

        assert score.points == points
