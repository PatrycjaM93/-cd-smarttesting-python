import logging
from typing import Optional

import requests
from requests.exceptions import RequestException
from smarttesting.client.customer import Customer
from smarttesting.client.customer_verification_result import (
    CustomerVerificationResult,
    Status,
)

logger = logging.getLogger(__name__)


class BIKVerificationService:
    """Klient do komunikacji z Biurem Informacji Kredytowej.

    Poza domyślnym konstruktorem, posiada
    """

    _bik_service_url: str
    _session: requests.Session

    def __init__(
        self, bik_service_url: str, session: Optional[requests.Session] = None
    ) -> None:
        """Initializer pokazujący, że uzywanie wartości domyślnych z bibliotek,
        np. w requests może się źle skończyć.
        """
        self._bik_service_url = bik_service_url
        if session is None:
            session = requests.Session()
        self._session = session

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        """
        Główna metoda biznesowa. Weryfikuje czy dana osoba jest oszustem poprzez
        wysłanie zapytania po HTTP do BIK. Do wykonania zapytania po HTTP
        wykorzystujemy bibliotekę `requests`.
        """
        try:
            id_number = customer.person.national_id_number
            response = self._session.get(self._bik_service_url + id_number)

            if response.text == Status.VERIFICATION_PASSED.name:
                return CustomerVerificationResult.create_passed(customer.uuid)
        except RequestException as exc:
            self._process_exception(exc)

        return CustomerVerificationResult.create_failed(customer.uuid)

    def _process_exception(self, exception: BaseException) -> None:
        logger.exception("HTTP request failed", exc_info=exception)
