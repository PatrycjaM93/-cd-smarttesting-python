from typing import Literal

from injector import Module, provider
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.personal.occupation_repository import OccupationRepository
from smarttesting.bik.score.personal.personal_information import (
    Education,
    Occupation,
    PersonalInformation,
)
from smarttesting.bik.score.personal.personal_information_client import (
    PersonalInformationClient,
)
from smarttesting.bik.score.personal.personal_information_score_evaluation import (
    PersonalInformationScoreEvaluation,
)


class Personal(Module):
    def __init__(self, env: Literal["PROD", "DEV"]) -> None:
        self._env = env

    @provider
    def personal_information_client(self) -> PersonalInformationClient:
        if self._env == "PROD":
            return PersonalInformationClient(
                personal_information_service_url="http://localhost:2345"
            )
        elif self._env == "DEV":
            return DevPersonalInformationClient()

    @provider
    def occupation_repo(self) -> OccupationRepository:
        if self._env == "PROD":
            raise NotImplementedError("TODO - sqlalchemy!")
        elif self._env == "DEV":
            return DevOccupationRepository()

    @provider
    def personal_info_score_evaluation(
        self, client: PersonalInformationClient, repository: OccupationRepository
    ) -> PersonalInformationScoreEvaluation:
        return PersonalInformationScoreEvaluation(client, repository)


class DevOccupationRepository(OccupationRepository):
    def get_occupation_scores(self) -> dict[Occupation, Score]:
        return {Occupation.DOCTOR: Score(100)}


class DevPersonalInformationClient(PersonalInformationClient):
    def __init__(self) -> None:
        pass

    def get_personal_information(self, pesel: Pesel) -> PersonalInformation | None:
        return PersonalInformation(Education.BASIC, 10, Occupation.DOCTOR)
