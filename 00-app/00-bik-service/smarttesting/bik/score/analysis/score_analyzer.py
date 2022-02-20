import logging

from smarttesting.bik.score.analysis.composite_score_evaluation import (
    CompositeScoreEvaluation,
)
from smarttesting.bik.score.domain.pesel import Pesel

logger = logging.getLogger(__name__)


class ScoreAnalyzer:

    # meter registry z io.micrometer.core.instrument.MeterRegistry (prometheus???)
    def __init__(
        self, composite_score_evaluation: CompositeScoreEvaluation, threshold: int
    ) -> None:
        self._composite_score_evaluation = composite_score_evaluation
        self._threshold = threshold
        # 		this.distributionSummary = DistributionSummary.builder("score.aggregated")
        # 				.publishPercentiles(0.5, 0.99)
        # 				.publishPercentileHistogram()
        # 				.register(meterRegistry);

    def should_grant_loan(self, pesel: Pesel) -> bool:
        aggregate_score = self._composite_score_evaluation.aggregate_all_scores(pesel)
        points = aggregate_score.points
        # distributionSummary.record(points)
        above_threshold = points >= self._threshold
        logger.info(
            "For PESEL %s we got score %d. "
            "It's %s that it's above or equal to the threshold %d",
            pesel,
            points,
            above_threshold,
            self._threshold,
        )
        return above_threshold
