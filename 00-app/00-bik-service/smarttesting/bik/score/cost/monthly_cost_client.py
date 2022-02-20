import logging
from decimal import Decimal
from urllib.parse import urljoin

import requests
from smarttesting.bik.score.domain.pesel import Pesel

logger = logging.getLogger(__name__)


class MonthlyCostClient:
    def __init__(self, monthly_cost_service_url: str) -> None:
        self._monthly_cost_service_url = monthly_cost_service_url

    def get_monthly_costs(self, pesel: Pesel) -> Decimal:
        url = urljoin(self._monthly_cost_service_url, pesel.pesel)
        monthly_cost_string = requests.get(url).text
        logger.info(
            "Monthly cost for id %s is %s",
            pesel,
            monthly_cost_string,
        )
        return Decimal(monthly_cost_string)
