from typing import Literal

from injector import Module, provider
from pymongo.database import Database
from smarttesting.bik.score.credit.credit_info import CreditInfo
from smarttesting.bik.score.credit.credit_info_repository import CreditInfoRepository
from smarttesting.bik.score.credit.credit_info_score_evaluation import (
    CreditInfoScoreEvaluation,
)
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.web.credit.mongo_credit_repository import (
    MongoCreditInfoRepository,
)


class Credit(Module):
    def __init__(self, env: Literal["DEV", "PROD"]) -> None:
        self._env = env

    @provider
    def credit_info_repository(self, mongo_db: Database) -> CreditInfoRepository:
        if self._env == "DEV":
            return DevCreditInfoRepository()
        elif self._env == "PROD":
            return MongoCreditInfoRepository(mongo_db)

    @provider
    def credit_info_score_evaluation(
        self, credit_info_repository: CreditInfoRepository
    ) -> CreditInfoScoreEvaluation:
        return CreditInfoScoreEvaluation(credit_info_repository)


class DevCreditInfoRepository(CreditInfoRepository):
    def __init__(self) -> None:
        self._dict = {}

    def find_credit_info(self, pesel: Pesel) -> CreditInfo | None:
        return self._dict.get(pesel)

    def save_credit_info(self, pesel: Pesel, credit_info: CreditInfo) -> CreditInfo:
        self._dict[pesel] = credit_info
        return credit_info
