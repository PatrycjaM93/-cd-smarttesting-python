from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.score_evaluation import ScoreEvaluation
from smarttesting.bik.score.social.social_status import (
    ContractType,
    MaritalStatus,
    SocialStatus,
)
from smarttesting.bik.score.social.social_status_client import SocialStatusClient


class SocialStatusScoreEvaluation(ScoreEvaluation):
    def __init__(self, client: SocialStatusClient) -> None:
        self._client = client

    def evaluate(self, pesel: Pesel) -> Score:
        social_status = self._client.get_social_status(pesel)
        return (
            Score.zero()
            + self._score_for_no_of_dependants(social_status)
            + self._score_for_no_of_people_in_the_household(social_status)
            + self._score_for_marital_status(social_status)
            + self._score_for_contract_type(social_status)
        )

    def _score_for_no_of_dependants(self, social_status: SocialStatus) -> Score:
        if social_status.no_of_dependants == 0:
            return Score(50)
        elif social_status.no_of_dependants == 1:
            return Score(40)
        elif social_status.no_of_dependants == 2:
            return Score(30)
        elif social_status.no_of_dependants == 3:
            return Score(20)
        elif social_status.no_of_dependants == 4:
            return Score(10)

        return Score.zero()

    def _score_for_no_of_people_in_the_household(
        self, social_status: SocialStatus
    ) -> Score:
        if social_status.no_of_people_in_the_household == 1:
            return Score(50)
        elif 1 < social_status.no_of_people_in_the_household <= 2:
            return Score(40)
        elif 2 < social_status.no_of_people_in_the_household < 3:
            return Score(30)
        elif 3 < social_status.no_of_people_in_the_household <= 4:
            return Score(20)
        elif 4 < social_status.no_of_people_in_the_household <= 5:
            return Score(10)

        return Score.zero()

    def _score_for_marital_status(self, social_status: SocialStatus) -> Score:
        if social_status.marital_status == MaritalStatus.SINGLE:
            return Score(20)
        elif social_status.marital_status == MaritalStatus.MARRIED:
            return Score(10)

    def _score_for_contract_type(self, social_status: SocialStatus) -> Score:
        if social_status.contract_type == ContractType.EMPLOYMENT_CONTRACT:
            return Score(20)
        elif social_status.contract_type == ContractType.OWN_BUSINESS_ACTIVITY:
            return Score(10)

        return Score.zero()
