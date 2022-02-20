from typing import Literal

from injector import Module, provider
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.social.social_status import (
    ContractType,
    MaritalStatus,
    SocialStatus,
)
from smarttesting.bik.score.social.social_status_client import SocialStatusClient
from smarttesting.bik.score.social.social_status_score_evaluation import (
    SocialStatusScoreEvaluation,
)


class Social(Module):
    def __init__(self, env: Literal["DEV", "PROD"]) -> None:
        self._env = env

    @provider
    def social_status_client(self) -> SocialStatusClient:
        if self._env == "PROD":
            return SocialStatusClient(social_status_service_url="http://localhost:4567")
        elif self._env == "DEV":
            return DevSocialStatusClient()

    @provider
    def social_score_evaluation(
        self, client: SocialStatusClient
    ) -> SocialStatusScoreEvaluation:
        return SocialStatusScoreEvaluation(client)


class DevSocialStatusClient(SocialStatusClient):
    def __init__(self) -> None:
        pass

    def get_social_status(self, pesel: Pesel) -> SocialStatus | None:
        return SocialStatus(
            1, 2, MaritalStatus.MARRIED, ContractType.EMPLOYMENT_CONTRACT
        )
