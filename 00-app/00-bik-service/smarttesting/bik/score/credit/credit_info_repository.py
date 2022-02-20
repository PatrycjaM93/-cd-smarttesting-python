import abc

from smarttesting.bik.score.credit.credit_info import CreditInfo
from smarttesting.bik.score.domain.pesel import Pesel


class CreditInfoRepository(abc.ABC):
    @abc.abstractmethod
    def find_credit_info(self, pesel: Pesel) -> CreditInfo | None:
        pass

    @abc.abstractmethod
    def save_credit_info(self, pesel: Pesel, credit_info: CreditInfo) -> CreditInfo:
        pass
