import logging
from decimal import Decimal

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.income.monthly_income_client import MonthlyIncomeClient
from smarttesting.bik.score.score_evaluation import ScoreEvaluation

logger = logging.getLogger(__name__)


class MonthlyIncomeScoreEvaluation(ScoreEvaluation):
    def __init__(self, client: MonthlyIncomeClient) -> None:
        self._client = client

    def evaluate(self, pesel: Pesel) -> Score:
        logger.info("Evaluating monthly income score for %s", pesel)
        monthly_income = self._client.get_monthly_income(pesel)
        # 0 - 500 - 0
        # 501 - 1500 - 10
        # 1501 - 3500 - 20
        # 3501 - 5500 - 30
        # 5501 - 10000 - 40
        # 10000 > 50
        if Decimal(0) <= monthly_income <= Decimal(500):
            return Score.zero()
        elif Decimal(501) <= monthly_income <= Decimal(1500):
            return Score(10)
        elif Decimal(1501) <= monthly_income <= Decimal(3500):
            return Score(20)
        elif Decimal(5501) <= monthly_income <= Decimal(10_000):
            return Score(40)

        return Score(50)
