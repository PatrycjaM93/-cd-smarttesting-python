import abc

from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.personal.personal_information import Occupation


class OccupationRepository(abc.ABC):
    @abc.abstractmethod
    def get_occupation_scores(self) -> dict[Occupation, Score]:
        pass
