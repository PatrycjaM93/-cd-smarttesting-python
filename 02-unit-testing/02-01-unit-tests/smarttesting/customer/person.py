import enum
from dataclasses import dataclass
from datetime import date


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Status(enum.Enum):
    STUDENT = "STUDENT"
    NOT_STUDENT = "NOT_STUDENT"


@dataclass
class Person:
    """Reprezentuje osobę do zweryfikowania."""

    _name: str
    _surname: str
    _date_of_birth: date
    _gender: Gender
    _national_id_number: str
    _status: Status = Status.NOT_STUDENT

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def date_of_birth(self) -> date:
        return self._date_of_birth

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def national_id_number(self) -> str:
        return self._national_id_number

    @property
    def is_student(self) -> bool:
        return self._status == Status.STUDENT

    def student(self) -> None:
        self._status = Status.STUDENT

    @property
    def age(self):
        today = date.today()
        years_diff = today.year - self._date_of_birth.year
        had_birthday_this_year = (
            today.replace(year=self._date_of_birth.year) < self._date_of_birth
        )
        if had_birthday_this_year:
            years_diff -= 1

        return years_diff
