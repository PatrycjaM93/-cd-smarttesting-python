import logging
from decimal import Decimal

from smarttesting.bik.score.cost.monthly_cost_client import MonthlyCostClient
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score

logger = logging.getLogger(__name__)


class MonthlyCostScoreEvaluation:
    def __init__(self, monthly_cost_client: MonthlyCostClient) -> None:
        self._monthly_cost_client = monthly_cost_client

    def evaluate(self, pesel: Pesel) -> Score:
        logger.info("Evaluating monthly cost score for %s", pesel)
        monthly_costs = self._monthly_cost_client.get_monthly_costs(pesel)
        # 0 - 500 - 50
        # 501 - 1500 - 40
        # 1501 - 3500 - 30
        # 3501 - 5500 - 20
        # 5501 - 10000 - 10
        # 10000 > 0
        if Decimal(0) <= monthly_costs < Decimal(500):
            return Score(50)
        elif Decimal(501) <= monthly_costs < Decimal(1500):
            return Score(40)
        elif Decimal(1501) <= monthly_costs < Decimal(3500):
            return Score(30)
        elif Decimal(5501) <= monthly_costs < Decimal(10_000):
            return Score(10)

        return Score.zero()
