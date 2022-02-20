from unittest.mock import Mock

import pytest
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.social.social_status import (
    ContractType,
    MaritalStatus,
    SocialStatus,
)
from smarttesting.bik.score.social.social_status_client import SocialStatusClient
from smarttesting.bik.score.social.social_status_score_evaluation import (
    SocialStatusScoreEvaluation,
)
from smarttesting.bik.score.social.validation.number_of_household_members_validation_exception import (
    NumberOfHouseholdMembersValidationException,
)
from tests.bik.score.utils import an_id


class TestSocialStatusScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._client = Mock(spec_set=SocialStatusClient)
        self._score_evaluation = SocialStatusScoreEvaluation(self._client)

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa None'a nie została zaimplementowana")
    )
    def test_returns_zero_when_null_social_status(self) -> None:
        self._client.get_social_status = Mock(return_value=None)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa None'a nie została zaimplementowana")
    )
    def test_returns_0_for_none_marital_status(self) -> None:
        social_status = SocialStatus(0, 0, None, ContractType.EMPLOYMENT_CONTRACT)
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa None'a nie została zaimplementowana")
    )
    def test_returns_0_for_none_employment_contract(self) -> None:
        social_status = SocialStatus(0, 0, MaritalStatus.MARRIED, None)
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi - logika nie została zaimplementowana "
            "Zazwyczaj w tego typu przypadkach testowych chcemy zweryfikować, "
            "w zależności od wymagań biznesowych, albo że jest rzucany odpowiedni wyjątek "
            "biznesowy albo że żaden wyjątek nie jest rzucony i błąd jest odpowiednio "
            "obsłużony w algorytmie (np. może być zwrócone Score.ZERO)"
        )
    )
    @pytest.mark.parametrize(
        "no_of_dependants, no_of_household_members",
        [
            (0, 0),
            (-1, 0),
            (0, -1),
            (2, 1),
            (1, 1),
        ],
    )
    def test_raises_business_exception_when_incorrect_numbers_of_members_dependants(
        self, no_of_dependants: int, no_of_household_members: int
    ) -> None:
        social_status = SocialStatus(
            no_of_dependants,
            no_of_household_members,
            MaritalStatus.SINGLE,
            ContractType.EMPLOYMENT_CONTRACT,
        )
        self._client.get_social_status = Mock(return_value=social_status)

        with pytest.raises(NumberOfHouseholdMembersValidationException):
            self._score_evaluation.evaluate(an_id())

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi: "
            "warunki brzegowe dla 3 członków gospodarstwa domowego niezaimplementowane "
            "poprawnie"
        )
    )
    @pytest.mark.parametrize(
        "no_of_household_members, points",
        [
            (1, 140),
            (2, 130),
            (3, 120),
            (4, 110),
            (5, 100),
            (6, 90),
            (0, 90),
        ],
    )
    def test_calculates_score_depending_on_number_of_household_members(
        self, no_of_household_members: int, points: int
    ) -> None:
        social_status = SocialStatus(
            0,
            no_of_household_members,
            MaritalStatus.SINGLE,
            ContractType.EMPLOYMENT_CONTRACT,
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(points)

    @pytest.mark.parametrize(
        "no_of_dependants, points",
        [
            (0, 90),
            (1, 80),
            (2, 70),
            (3, 60),
            (4, 50),
            (5, 40),
            (-1, 40),
        ],
    )
    def test_calculates_score_depending_on_number_of_dependants(
        self, no_of_dependants: int, points: int
    ) -> None:
        social_status = SocialStatus(
            no_of_dependants, 6, MaritalStatus.SINGLE, ContractType.EMPLOYMENT_CONTRACT
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(points)

    def test_calculates_score_for_single_customer(self) -> None:
        social_status = SocialStatus(
            0, 6, MaritalStatus.SINGLE, ContractType.EMPLOYMENT_CONTRACT
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(90)

    def test_calculates_score_for_married_and_with_employed_contract(self) -> None:
        social_status = SocialStatus(
            0, 6, MaritalStatus.MARRIED, ContractType.EMPLOYMENT_CONTRACT
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(80)

    def test_calculates_score_when_own_business(self) -> None:
        social_status = SocialStatus(
            0, 6, MaritalStatus.MARRIED, ContractType.OWN_BUSINESS_ACTIVITY
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(70)

    def test_calculates_score_when_unemployed(self) -> None:
        social_status = SocialStatus(
            0, 6, MaritalStatus.MARRIED, ContractType.UNEMPLOYED
        )
        self._client.get_social_status = Mock(return_value=social_status)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(60)
