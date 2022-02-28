import csv
from datetime import date, datetime
from pathlib import Path
from typing import Tuple

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identity_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.event_emitter import EventEmitter


def cases_from_csv(filename: str) -> list[Tuple[date, Gender, bool]]:
    """Używany niżej do odczytania przypadków testowych z pliku .csv."""
    path = Path(__file__).parents[4] / filename
    bool_mapping = {"true": True, "false": False}
    with open(path) as file:
        csv_reader = csv.DictReader(file)
        return [
            (
                datetime.strptime(row["birthDate"], "%Y-%m-%d").date(),
                getattr(Gender, (row["gender"])),
                bool_mapping[row["passes"]],
            )
            for row in csv_reader
        ]


class TestIdentificationNumberVerification:
    """Klasa zawiera przykłady testów parametryzowanych."""

    def test_passess_for_correct_identification_number(self) -> None:
        # given
        person = self._build_person(date(1998, 3, 14), Gender.FEMALE)
        verification = IdentificationNumberVerification(EventEmitter())

        # when
        passes = verification.passes(person)

        # then
        assert passes is True

    def test_fails_for_inconsistent_gender(self) -> None:
        # given
        person = self._build_person(date(1998, 3, 14), Gender.MALE)
        verification = IdentificationNumberVerification(EventEmitter())

        # when
        passes = verification.passes(person)

        # then
        assert passes is False

    def test_fails_for_wrong_year_of_birth(self) -> None:
        # given
        person = self._build_person(date(2000, 3, 14), Gender.FEMALE)
        verification = IdentificationNumberVerification(EventEmitter())

        # when
        passes = verification.passes(person)

        # then
        assert passes is False

    @pytest.mark.parametrize(
        "date_of_birth, gender, expected_passes",
        [
            (date(1998, 3, 14), Gender.FEMALE, True),
            (date(1998, 3, 14), Gender.MALE, False),
            (date(2000, 3, 14), Gender.FEMALE, False),
        ],
    )
    def test_verifies(
        self, date_of_birth: date, gender: Gender, expected_passes: bool
    ) -> None:
        # given
        person = self._build_person(date_of_birth, gender)
        verification = IdentificationNumberVerification(EventEmitter())

        # when
        actual_passes = verification.passes(person)

        # then
        assert actual_passes is expected_passes

    @pytest.fixture(params=cases_from_csv("resources/pesel.csv"))
    def date_gender_passes(self, request) -> Tuple[date, Gender, bool]:
        return request.param

    def test_verification_csv(
        self,
        date_gender_passes: Tuple[date, Gender, bool],
    ) -> None:
        """Test tych samych przypadków co w 3 różnych testach powyżej przy pomocy
        parametryzowanej fikstury, która jest zasilana z pliku CSV.
        """
        date_of_birth, gender, passes = date_gender_passes
        # Given
        person = self._build_person(date_of_birth, gender)
        verification = IdentificationNumberVerification(EventEmitter())

        # When
        result = verification.passes(person)

        # Then
        assert result is passes

    def _build_person(self, birth_date: date, gender: Gender) -> Person:
        return Person("John", "Doe", birth_date, gender, "98031416402")
