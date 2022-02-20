import enum
from dataclasses import dataclass


class MaritalStatus(enum.Enum):
    SINGLE = enum.auto()
    MARRIED = enum.auto()


class ContractType(enum.Enum):
    # UoP
    EMPLOYMENT_CONTRACT = enum.auto()
    # B2B
    OWN_BUSINESS_ACTIVITY = enum.auto()
    UNEMPLOYED = enum.auto()


@dataclass
class SocialStatus:
    """Liczba osób na utrzymaniu."""

    no_of_dependants: int | None

    """Liczba osób w gospodarstwie domowym."""
    no_of_people_in_the_household: int | None

    marital_status: MaritalStatus | None

    contract_type: ContractType | None
