import enum
from dataclasses import dataclass
from decimal import Decimal


class DebtPaymentHistory(enum.Enum):
    NOT_A_SINGLE_PAID_INSTALLMENT = enum.auto()
    MULTIPLE_UNPAID_INSTALLMENTS = enum.auto()
    INDIVIDUAL_UNPAID_INSTALLMENTS = enum.auto()
    NOT_A_SINGLE_UNPAID_INSTALLMENT = enum.auto()


@dataclass
class CreditInfo:
    """
    Aktualne zadłużenie (spłacane kredyty, pożyczki, ale także posiadane
    karty kredytowe czy limity w rachunku, ze szczególnym uwzględnieniem
    wysokości raty innych kredytów)
    """

    current_debt: Decimal | None

    """Koszty utrzymania kredytobiorcy i jego rodziny."""
    current_living_costs: Decimal | None

    """
    Historia kredytowa 
    (sposób, w jaki kredytobiorca spłacał dotychczasowe zobowiązania).
    """
    debt_payment_history: DebtPaymentHistory | None
