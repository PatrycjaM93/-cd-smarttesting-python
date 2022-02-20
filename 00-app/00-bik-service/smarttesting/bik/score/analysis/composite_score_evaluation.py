import abc

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score


class CompositeScoreEvaluation(abc.ABC):
    @abc.abstractmethod
    def aggregate_all_scores(self, pesel: Pesel) -> Score:
        pass
