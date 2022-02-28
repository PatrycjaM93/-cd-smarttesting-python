import enum


class LoanType(enum.Enum):
    """Typ pożyczki: studencka bądź zwykła."""

    STUDENT = "STUDENT"
    REGULAR = "REGULAR"
