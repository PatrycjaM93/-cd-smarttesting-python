import abc

from smarttesting.bik.score.domain.score_calculated_event import ScoreCalculatedEvent


class ScoreUpdater(abc.ABC):
    @abc.abstractmethod
    def score_calculated(self, score_calculated_event: ScoreCalculatedEvent) -> None:
        pass
