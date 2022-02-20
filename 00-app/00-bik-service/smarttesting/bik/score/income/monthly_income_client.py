import logging
from decimal import Decimal
from urllib.parse import urljoin

import requests
from smarttesting.bik.score.domain.pesel import Pesel

logger = logging.getLogger(__name__)


class MonthlyIncomeClient:
    def __init__(self, monthly_income_service_url: str) -> None:
        self._monthly_income_service_url = monthly_income_service_url

    def get_monthly_income(self, pesel: Pesel) -> Decimal | None:
        url = urljoin(self._monthly_income_service_url, pesel.pesel)
        response = requests.get(url).text
        monthly_income = Decimal(response)
        logger.info("Monthly income for id %s is %s", pesel, monthly_income)
        return monthly_income
