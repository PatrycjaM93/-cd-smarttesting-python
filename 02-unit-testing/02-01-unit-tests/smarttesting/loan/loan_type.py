import enum


class LoanType(enum.Enum):
    """Typ pożyczki: studencka bądź zwykła."""

    STUDENT = enum.auto()
    REGULAR = enum.auto()
