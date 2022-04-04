import logging
import time
from dataclasses import dataclass

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)

logger = logging.getLogger(__name__)


@dataclass
class BIKVerificationService:
    _bik_service_url: str

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        try:
            time.sleep(0.3)
            return self.create_passed(customer)
        except Exception:
            logger.exception("HTTP request execution failed!")

        return CustomerVerificationResult.create_failed(customer.uuid)

    def create_passed(self, customer: Customer) -> CustomerVerificationResult:
        return CustomerVerificationResult.create_passed(customer.uuid)

    def complex_method(self, a: int, b: int, c: int) -> int:
        """Sztucznie skomplikowana metoda.

        Ukazuje wysoki poziom skomplikowania cyklomatycznego.
        """
        d = a + 2
        e = d + 5 if a > 0 else c
        f = e + 5 if d > 0 else a
        result = 0
        if a > b or f > 1 and d + 1 > 3 or f < 4:
            return 8
        if a > c and e > f or a > 1 and e + 1 > 3 or d < 4:
            return 1
        else:
            if a + 1 > c - 1 or a > b + 3 or f > 19:
                return 1233
            if e < a and d > c:
                if a + 4 > b - 2:
                    if c - 5 < a + 11:
                        return 81
                    elif a > c:
                        return 102
                if a > c + 21 and e > f - 12:
                    return 13
                else:
                    if a + 10 > c - 1:
                        return 123
                    elif e + 1 < a and d + 14 > c:
                        return 111
                    if f > 10:
                        return 1

            return result
