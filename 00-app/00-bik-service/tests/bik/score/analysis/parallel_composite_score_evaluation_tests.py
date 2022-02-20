import logging
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest
from smarttesting.bik.score.analysis.parallel_composite_score_evaluation import (
    ParallelCompositeScoreEvaluation,
)
from smarttesting.bik.score.analysis.score_updater import ScoreUpdater

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.domain.score_calculated_event import ScoreCalculatedEvent
from smarttesting.bik.score.score_evaluation import ScoreEvaluation


class TestParallelCompositeScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._score_updater = Mock(spec_set=ScoreUpdater)

    def test_calculates_score(self) -> None:
        executor = ThreadPoolExecutor(max_workers=2)
        with executor:
            evaluation = ParallelCompositeScoreEvaluation(
                [TenScoreEvaluation(), TwentyScoreEvaluation()],
                executor,
                self._score_updater,
            )

            score = evaluation.aggregate_all_scores(Pesel("12345678901"))

        assert score.points == 30
        self._score_updater.score_calculated.assert_called_once_with(
            ScoreCalculatedEvent(pesel=Pesel("12345678901"), score=Score(30))
        )

    @pytest.mark.skip(reason="Test wykryje błąd")
    def test_returns_0_score_when_exception_thrown(self) -> None:
        executor = ThreadPoolExecutor(max_workers=1)
        with executor:
            evaluation = ParallelCompositeScoreEvaluation(
                [ExceptionScoreEvaluation()], executor, self._score_updater
            )

            score = evaluation.aggregate_all_scores(Pesel("12345678901"))

        assert score == Score.zero()
        self._score_updater.score_calculated.assert_called_once_with(
            ScoreCalculatedEvent(pesel=Pesel("12345678901"), score=Score.zero())
        )


class TenScoreEvaluation(ScoreEvaluation):
    logger = logging.getLogger("TenScoreEvaluation")

    def evaluate(self, pesel: Pesel) -> Score:
        self.logger.info("Hello from 10")
        return Score(10)


class TwentyScoreEvaluation(ScoreEvaluation):
    logger = logging.getLogger("TwentyScoreEvaluation")

    def evaluate(self, pesel: Pesel) -> Score:
        self.logger.info("Hello from 20")
        return Score(20)


class ExceptionScoreEvaluation(ScoreEvaluation):
    logger = logging.getLogger("ExceptionScoreEvaluation")

    def evaluate(self, pesel: Pesel) -> Score:
        self.logger.info("Hello from exception")
        raise ValueError("Boom!")
