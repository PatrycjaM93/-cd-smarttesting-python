import logging
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import List, Literal

from injector import Module, provider
from kombu import Connection
from smarttesting.bik.score.analysis.composite_score_evaluation import (
    CompositeScoreEvaluation,
)
from smarttesting.bik.score.analysis.parallel_composite_score_evaluation import (
    ParallelCompositeScoreEvaluation,
)
from smarttesting.bik.score.analysis.score_analyzer import ScoreAnalyzer
from smarttesting.bik.score.analysis.score_updater import ScoreUpdater
from smarttesting.bik.score.domain.score_calculated_event import ScoreCalculatedEvent
from smarttesting.bik.score.score_evaluation import ScoreEvaluation
from smarttesting.bik.web.analysis.rabbit_credit_score_updater import (
    RabbitCreditScoreUpdater,
)


class Analysis(Module):
    def __init__(self, env: Literal["DEV", "PROD"], threshold: int = 500) -> None:
        self._env = env
        self._threshold = threshold

    @provider
    def composite_score_evaluation(
        self,
        score_evaluations: List[ScoreEvaluation],
        executor: Executor,
        score_updater: ScoreUpdater,
    ) -> CompositeScoreEvaluation:
        return ParallelCompositeScoreEvaluation(
            score_evaluations, executor, score_updater
        )

    @provider
    def score_analyzer(
        self, composite_score_evaluation: CompositeScoreEvaluation
    ) -> ScoreAnalyzer:
        return ScoreAnalyzer(composite_score_evaluation, self._threshold)

    @provider
    def score_updater(self, connection: Connection) -> ScoreUpdater:
        if self._env == "DEV":
            return DevCreditScoreUpdater()
        elif self._env == "PROD":
            return RabbitCreditScoreUpdater(connection)

    @provider
    def executor(self) -> Executor:
        return ThreadPoolExecutor(max_workers=2)


class DevCreditScoreUpdater(ScoreUpdater):
    def score_calculated(self, score_calculated_event: ScoreCalculatedEvent) -> None:
        logger = logging.getLogger(type(self).__name__)
        logger.info("Got the event %s", score_calculated_event)
