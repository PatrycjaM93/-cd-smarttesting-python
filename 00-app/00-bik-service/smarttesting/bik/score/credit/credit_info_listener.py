import abc

from smarttesting.bik.score.credit.credit_info import CreditInfo
from smarttesting.bik.score.domain.pesel import Pesel


class CreditInfoListener(abc.ABC):
    @abc.abstractmethod
    def store_credit_info(self, pesel: Pesel, credit_info: CreditInfo) -> None:
        pass
