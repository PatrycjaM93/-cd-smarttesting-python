from unittest.mock import Mock

import pytest
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
from tests.bik.score.utils import an_id


class TestPersonalInformationScoreEvaluation:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._client = Mock(spec_set=PersonalInformationClient)
        self._score_evaluation = PersonalInformationScoreEvaluation(
            self._client, StubOccupationRepository()
        )

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa None'ów nie została zaimplementowana")
    )
    def test_returns_zero_when_none_personal_information(self) -> None:
        self._client.get_personal_information = Mock(return_value=None)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=("Test nie przechodzi; obsługa None'ów nie została zaimplementowana")
    )
    def test_returns_zero_when_nones_in_personal_information(self) -> None:
        personal_info = PersonalInformation(None, 0, None)
        self._client.get_perwsonal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    @pytest.mark.skip(
        reason=(
            "Test nie przechodzi - obrakuje implementacji dla > 30 lat doświadczenia"
        )
    )
    @pytest.mark.parametrize(
        "years_of_work_experience, points",
        [
            (-2, 0),
            (0, 0),
            (1, 5),
            (2, 10),
            (4, 10),
            (5, 20),
            (7, 20),
            (9, 20),
            (10, 30),
            (11, 30),
            (14, 30),
            (15, 40),
            (17, 40),
            (19, 40),
            (20, 50),
            (21, 50),
            (29, 50),
            (30, 60),
            (45, 60),
        ],
    )
    def test_calculates_score_based_on_years_of_experience(
        self, years_of_work_experience: int, points: int
    ) -> None:
        personal_info = PersonalInformation(
            Education.NONE, years_of_work_experience, Occupation.OTHER
        )
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(points)

    def test_calculates_score_when_occupation_present_in_repo(self) -> None:
        personal_info = PersonalInformation(Education.NONE, 0, Occupation.PROGRAMMER)
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(30)

    def test_calculates_score_0_when_occupation_not_in_repo_and_no_education(
        self,
    ) -> None:
        personal_info = PersonalInformation(Education.NONE, 0, Occupation.DOCTOR)
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score.zero()

    def test_calculates_score_for_basic_education(self) -> None:
        personal_info = PersonalInformation(Education.BASIC, 0, Occupation.DOCTOR)
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(10)

    def test_calculates_score_for_medium_education(self) -> None:
        personal_info = PersonalInformation(Education.MEDIUM, 0, Occupation.DOCTOR)
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(30)

    def test_calculates_score_for_high_education(self) -> None:
        personal_info = PersonalInformation(Education.HIGH, 0, Occupation.DOCTOR)
        self._client.get_personal_information = Mock(return_value=personal_info)

        score = self._score_evaluation.evaluate(an_id())

        assert score == Score(50)


class StubOccupationRepository(OccupationRepository):
    """Test double typu Stub dla OccupationRepository.

    Dodaliśmy tylko jeden zawód do słownika, gdyż na potrzeby tych testow interesują
    nas tylko dwie sytuacje:
    1) dany zawód jest w repozytorium
    2) danego zawodu nie ma w repozytorium
    """

    def get_occupation_scores(self) -> dict[Occupation, Score]:
        return {Occupation.PROGRAMMER: Score(30)}
