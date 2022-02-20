from typing import Literal

from injector import Module, provider
from smarttesting.bik.score.cost.monthly_cost_client import MonthlyCostClient
from smarttesting.bik.score.cost.monthly_cost_score_evaluation import (
    MonthlyCostScoreEvaluation,
)


class Cost(Module):
    def __init__(self, env: Literal["DEV", "PROD"]) -> None:
        self._env = env

    @provider
    def monthly_cost_client(self) -> MonthlyCostClient:
        return MonthlyCostClient(monthly_cost_service_url="http://localhost:3456")

    @provider
    def monthly_cost_score_evaluation(
        self, monthly_cost_client: MonthlyCostClient
    ) -> MonthlyCostScoreEvaluation:
        return MonthlyCostScoreEvaluation(monthly_cost_client)
