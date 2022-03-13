import enum
from datetime import date
from uuid import UUID

from pydantic import BaseModel


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Status(enum.Enum):
    STUDENT = "STUDENT"
    NOT_STUDENT = "NOT_STUDENT"


class Person(BaseModel):
    """Reprezentuje osobę do zweryfikowania."""

    uuid: UUID
    name: str
    surname: str
    date_of_birth: date
    gender: Gender
    national_id_number: str
    status: Status = Status.NOT_STUDENT

    @property
    def is_student(self) -> bool:
        return self.status == Status.STUDENT

    def student(self) -> None:
        self.status = Status.STUDENT

    @property
    def age(self):
        today = date.today()
        years_diff = today.year - self.date_of_birth.year
        had_birthday_this_year = (
            today.replace(year=self.date_of_birth.year) < self.date_of_birth
        )
        if had_birthday_this_year:
            years_diff -= 1

        return years_diff
