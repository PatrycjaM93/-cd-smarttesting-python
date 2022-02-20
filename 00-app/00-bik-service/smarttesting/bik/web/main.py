from typing import List, Literal

from injector import Injector, Module, multiprovider, provider, singleton
from kombu import Connection
from pymongo import MongoClient
from pymongo.database import Database
from smarttesting.bik.score.credit.credit_info_score_evaluation import (
    CreditInfoScoreEvaluation,
)
from smarttesting.bik.score.income.monthly_income_score_evaluation import (
    MonthlyIncomeScoreEvaluation,
)
from smarttesting.bik.score.personal.personal_information_score_evaluation import (
    PersonalInformationScoreEvaluation,
)
from smarttesting.bik.score.score_evaluation import ScoreEvaluation
from smarttesting.bik.score.social.social_status_score_evaluation import (
    SocialStatusScoreEvaluation,
)
from smarttesting.bik.web.analysis.module import Analysis
from smarttesting.bik.web.cost.module import Cost
from smarttesting.bik.web.credit.module import Credit
from smarttesting.bik.web.income.module import Income
from smarttesting.bik.web.personal.module import Personal
from smarttesting.bik.web.social.module import Social


def assemble(env: Literal["DEV", "PROD"] = "DEV") -> Injector:
    return Injector(
        [
            Analysis(env),
            Cost(env),
            Credit(env),
            Income(env),
            Personal(env),
            Social(env),
            CombinedScoreEvaluations(),
            Mongo(),
            RabbitMq(),
        ],
        auto_bind=False,
    )


class CombinedScoreEvaluations(Module):
    @multiprovider
    def score_evaluations(
        self,
        credit: CreditInfoScoreEvaluation,
        income: MonthlyIncomeScoreEvaluation,
        personal_info: PersonalInformationScoreEvaluation,
        social: SocialStatusScoreEvaluation,
    ) -> List[ScoreEvaluation]:
        return [credit, income, personal_info, social]


class Mongo(Module):
    @singleton
    @provider
    def database(self) -> Database:
        client = MongoClient()
        return client.get_database("bik_database")


class RabbitMq(Module):
    @provider
    def connection(self) -> Connection:
        return Connection()
