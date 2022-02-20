import abc

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score


class ScoreEvaluation(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, pesel: Pesel) -> Score:
        pass
