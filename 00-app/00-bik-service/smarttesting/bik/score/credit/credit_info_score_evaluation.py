import logging
from decimal import Decimal

from smarttesting.bik.score.credit.credit_info import DebtPaymentHistory
from smarttesting.bik.score.credit.credit_info_repository import CreditInfoRepository
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score
from smarttesting.bik.score.score_evaluation import ScoreEvaluation

logger = logging.getLogger(__name__)


class CreditInfoScoreEvaluation(ScoreEvaluation):
    def __init__(self, credit_info_repository: CreditInfoRepository) -> None:
        self._credit_info_repository = credit_info_repository

    def evaluate(self, pesel: Pesel) -> Score:
        logger.info("Evaluating credit info score for %s", pesel)
        credit_info = self._credit_info_repository.find_credit_info(pesel)
        if credit_info is None:
            return Score.zero()

        return (
            Score.zero()
            + self._score_for_current_debt(credit_info.current_debt)
            + self._score_for_current_living_costs(credit_info.current_living_costs)
            + self._score_for_debt_payment_history(credit_info.debt_payment_history)
        )

    def _score_for_current_debt(self, current_debt: Decimal) -> Score:
        if Decimal(5501) <= current_debt <= Decimal(10000):
            return Score.zero()
        elif Decimal(3501) <= current_debt <= Decimal(5500):
            return Score(10)
        elif Decimal(1501) <= current_debt <= Decimal(3500):
            return Score(20)
        elif Decimal(500) <= current_debt <= Decimal(1500):
            return Score(40)

        return Score(50)

    def _score_for_current_living_costs(self, current_living_costs: Decimal) -> Score:
        if Decimal(6501) <= current_living_costs <= Decimal(10000):
            return Score.zero()
        elif Decimal(4501) <= current_living_costs <= Decimal(6500):
            return Score(10)
        elif Decimal(2501) <= current_living_costs <= Decimal(4500):
            return Score(20)
        elif Decimal(1000) <= current_living_costs <= Decimal(2500):
            return Score(40)
        else:
            return Score(50)

    def _score_for_debt_payment_history(
        self, debt_payment_history: DebtPaymentHistory
    ) -> Score:
        if debt_payment_history == DebtPaymentHistory.MULTIPLE_UNPAID_INSTALLMENTS:
            return Score(10)
        elif debt_payment_history == DebtPaymentHistory.NOT_A_SINGLE_UNPAID_INSTALLMENT:
            return Score(50)
        elif debt_payment_history == DebtPaymentHistory.INDIVIDUAL_UNPAID_INSTALLMENTS:
            return Score(30)

        return Score.zero()
