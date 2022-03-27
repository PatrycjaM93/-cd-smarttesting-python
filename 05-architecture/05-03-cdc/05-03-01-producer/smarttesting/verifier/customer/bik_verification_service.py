import logging
from dataclasses import dataclass

import requests
from requests.exceptions import RequestException
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
    Status,
)

logger = logging.getLogger(__name__)


@dataclass
class BIKVerificationService:
    """Klient do komunikacji z Biurem Informacji Kredytowej."""

    _bik_service_url: str

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        """
        Weryfikuje czy dana osoba jest oszustem poprzez wysłanie zapytania po HTTP
        do BIK. Do wykonania zapytania po HTTP wykorzystujemy bibliotekę `requests`.
        """
        try:
            id_number = customer.person.national_id_number
            response = requests.get(self._bik_service_url + id_number)

            if response.text == Status.VERIFICATION_PASSED.name:
                return CustomerVerificationResult.create_passed(customer.uuid)
        except RequestException:
            logger.exception("HTTP request failed")

        return CustomerVerificationResult.create_failed(customer.uuid)
