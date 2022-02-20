from decimal import Decimal
from typing import Literal

from injector import Module, provider
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.income.monthly_income_client import MonthlyIncomeClient
from smarttesting.bik.score.income.monthly_income_score_evaluation import (
    MonthlyIncomeScoreEvaluation,
)


class Income(Module):
    def __init__(self, env: Literal["DEV", "PROD"]) -> None:
        self._env = env

    @provider
    def monthly_income_client(self) -> MonthlyIncomeClient:
        if self._env == "PROD":
            return MonthlyIncomeClient(
                monthly_income_service_url="http://localhost:1234"
            )
        elif self._env == "DEV":
            return DevMonthlyIncomeClient()

    @provider
    def monthly_score_evaluation(
        self, monthly_income_client: MonthlyIncomeClient
    ) -> MonthlyIncomeScoreEvaluation:
        return MonthlyIncomeScoreEvaluation(monthly_income_client)


class DevMonthlyIncomeClient(MonthlyIncomeClient):
    def __init__(self) -> None:
        pass

    def get_monthly_income(self, pesel: Pesel) -> Decimal | None:
        return Decimal("2000")
