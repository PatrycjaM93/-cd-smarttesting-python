import logging

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.personal.occupation_repository import OccupationRepository
from smarttesting.bik.score.personal.personal_information import Education, Occupation
from smarttesting.bik.score.personal.personal_information_client import (
    PersonalInformationClient,
)
from smarttesting.bik.score.score_evaluation import ScoreEvaluation

logger = logging.getLogger(__name__)


class PersonalInformationScoreEvaluation(ScoreEvaluation):
    def __init__(
        self,
        client: PersonalInformationClient,
        occupation_repository: OccupationRepository,
    ) -> None:
        self._client = client
        self._occupation_repository = occupation_repository

    def evaluate(self, pesel: Pesel) -> Score:
        logger.info("Evaluating personal info score for %s", pesel)
        personal_info = self._client.get_personal_information(pesel)
        return (
            Score.zero()
            + self._score_for_occupation(personal_info.occupation)
            + self._score_for_education(personal_info.education)
            + self._score_for_years_of_work_experience(
                personal_info.years_of_work_experience
            )
        )

    def _score_for_occupation(self, occupation: Occupation) -> Score:
        occupation_to_score = self._occupation_repository.get_occupation_scores()
        logger.info("Found following mappings %r", occupation_to_score)
        score = occupation_to_score.get(occupation)
        logger.info("Found score %r for occupation %s", score, occupation)
        return score if score is not None else Score.zero()

    def _score_for_education(self, education: Education) -> Score:
        if education == Education.BASIC:
            return Score(10)
        elif education == Education.HIGH:
            return Score(50)
        elif education == Education.MEDIUM:
            return Score(30)

        return Score.zero()

    def _score_for_years_of_work_experience(
        self, years_of_work_experience: int
    ) -> Score:
        if years_of_work_experience == 1:
            return Score(5)
        elif 2 <= years_of_work_experience < 5:
            return Score(10)
        elif 5 <= years_of_work_experience < 10:
            return Score(20)
        elif 10 <= years_of_work_experience < 15:
            return Score(30)
        elif 15 <= years_of_work_experience < 20:
            return Score(40)
        elif 20 <= years_of_work_experience < 30:
            return Score(50)

        return Score.zero()
