import csv
from datetime import date, datetime
from pathlib import Path
from typing import List, Tuple

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.event_emitter import EventEmitter
from tests.verifier.customer.factories import PersonFactory


def build_person(date_of_birth: date, gender: Gender) -> Person:
    return PersonFactory.build(
        name="John",
        surname="Doe",
        date_of_birth=date_of_birth,
        gender=gender,
        national_id_number="98031416402",
    )


def cases_from_csv(filename: str) -> List[Tuple[date, Gender, bool]]:
    """Używany niżej do odczytania przypadków testowych z pliku .csv."""
    path = Path(__file__).parent / filename
    bool_mapping = {"true": True, "false": False}
    with open(path) as file:
        csv_reader = csv.DictReader(file)
        return [
            (
                datetime.strptime(row["birthDate"], "%Y-%m-%d").date(),
                Gender(row["gender"]),
                bool_mapping[row["passes"]],
            )
            for row in csv_reader
        ]


class TestIdentificationNumberVerification:
    @pytest.fixture()
    def verification(self) -> IdentificationNumberVerification:
        return IdentificationNumberVerification(EventEmitter())

    def test_passes_for_correct_identification_number(
        self, verification: IdentificationNumberVerification
    ) -> None:
        # Given
        person = build_person(date(1998, 3, 14), Gender.FEMALE)

        # When
        passes = verification.passes(person)

        # Then
        assert passes is True

    def test_fails_for_inconsistent_gender(
        self, verification: IdentificationNumberVerification
    ) -> None:
        # Given
        person = build_person(date(1998, 3, 14), Gender.MALE)

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False

    def test_fails_for_wrong_year_of_birth(
        self, verification: IdentificationNumberVerification
    ) -> None:
        # Given
        person = build_person(date(2000, 3, 14), Gender.FEMALE)

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False

    @pytest.mark.parametrize(
        "date_of_birth, gender, passes",
        [
            (date(1998, 3, 14), Gender.FEMALE, True),
            (date(1998, 3, 14), Gender.MALE, False),
            (date(2000, 3, 14), Gender.FEMALE, False),
        ],
    )
    def test_verification(
        self,
        date_of_birth: date,
        gender: Gender,
        passes: bool,
        verification: IdentificationNumberVerification,
    ) -> None:
        """Test tych samych przypadków co w 3 różnych testach powyżej przy pomocy
        parametryzacji testu.
        """
        # Given
        person = build_person(date_of_birth, gender)

        # When
        result = verification.passes(person)

        # Then
        assert result is passes

    @pytest.fixture(params=cases_from_csv("fixtures/pesel.csv"))
    def date_gender_passes(self, request) -> Tuple[date, Gender, bool]:
        return request.param

    def test_verification_csv(
        self,
        date_gender_passes: Tuple[date, Gender, bool],
        verification: IdentificationNumberVerification,
    ) -> None:
        """Test tych samych przypadków co w 3 różnych testach powyżej przy pomocy
        parametryzowanej fikstury, która jest zasilana z pliku CSV.
        """
        date_of_birth, gender, passes = date_gender_passes
        # Given
        person = build_person(date_of_birth, gender)

        # When
        result = verification.passes(person)

        # Then
        assert result is passes
