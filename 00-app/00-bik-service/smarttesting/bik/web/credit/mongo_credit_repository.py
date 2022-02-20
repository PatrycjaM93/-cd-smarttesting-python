from decimal import Decimal

from pymongo.database import Database
from smarttesting.bik.score.credit.credit_info import CreditInfo, DebtPaymentHistory
from smarttesting.bik.score.credit.credit_info_repository import CreditInfoRepository
from smarttesting.bik.score.domain.pesel import Pesel


class MongoCreditInfoRepository(CreditInfoRepository):
    def __init__(self, mongo_db: Database) -> None:
        self._collection = mongo_db.credit_information

    def find_credit_info(self, pesel: Pesel) -> CreditInfo | None:
        document = self._collection.find_one({"pesel": pesel.pesel})
        if not document:
            return None
        else:
            return CreditInfo(
                current_debt=Decimal(document["current_debt"]),
                current_living_costs=Decimal(document["current_living_costs"]),
                debt_payment_history=getattr(
                    DebtPaymentHistory, document["debt_payment_history"]
                ),
            )

    def save_credit_info(self, pesel: Pesel, credit_info: CreditInfo) -> CreditInfo:
        self._collection.insert_one(
            {
                "pesel": pesel.pesel,
                "current_debt": str(credit_info.current_debt),
                "current_living_costs": str(credit_info.current_living_costs),
                "debt_payment_history": credit_info.debt_payment_history.name,
            }
        )
        return credit_info
