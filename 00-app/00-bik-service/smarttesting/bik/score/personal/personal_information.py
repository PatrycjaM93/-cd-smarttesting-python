import enum
from dataclasses import dataclass


class Education(enum.Enum):
    NONE = enum.auto()
    BASIC = enum.auto()
    MEDIUM = enum.auto()
    HIGH = enum.auto()


class Occupation(enum.Enum):
    PROGRAMMER = enum.auto()
    LAWYER = enum.auto()
    DOCTOR = enum.auto()
    OTHER = enum.auto()


@dataclass
class PersonalInformation:
    education: Education | None
    years_of_work_experience: int | None
    occupation: Occupation | None
