import logging
from concurrent.futures import Executor, as_completed

from smarttesting.bik.score.analysis.composite_score_evaluation import (
    CompositeScoreEvaluation,
)
from smarttesting.bik.score.analysis.score_updater import ScoreUpdater
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.domain.score_calculated_event import ScoreCalculatedEvent
from smarttesting.bik.score.score_evaluation import ScoreEvaluation

logger = logging.getLogger(__name__)


class ParallelCompositeScoreEvaluation(CompositeScoreEvaluation):
    def __init__(
        self,
        score_evaluations: list[ScoreEvaluation],
        executor: Executor,
        score_updater: ScoreUpdater,
    ) -> None:
        self._score_evaluations = score_evaluations
        self._executor = executor
        self._score_updater = score_updater

    def aggregate_all_scores(self, pesel: Pesel) -> Score:
        with self._executor:
            futures = []
            for score_evaluation in self._score_evaluations:
                future = self._executor.submit(score_evaluation.evaluate, pesel)
                futures.append(future)
            score = sum(
                [future.result() for future in as_completed(futures, timeout=60)],
                start=Score.zero(),
            )
            logger.info("Calculated score %r for pesel %s", score, pesel)
        self._score_updater.score_calculated(ScoreCalculatedEvent(pesel, score))
        return score
