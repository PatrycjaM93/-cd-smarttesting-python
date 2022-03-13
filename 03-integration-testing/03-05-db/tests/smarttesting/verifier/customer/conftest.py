import socket
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)


@pytest.fixture
def random_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    _address, number = sock.getsockname()
    sock.close()
    return number


@pytest.fixture
def exception_throwing_bik_identifier() -> BIKVerificationService:
    """Mock klasy odpowiedzialnej za komunikację z BIK.

    Rzuca wyjątkiem jeśli zostanie wywołana. W ten sposób upewniamy się, że test się
    wysypie jeśli spróbujemy zawołać BIK.
    """
    return Mock(
        spec_set=BIKVerificationService,
        verify=Mock(side_effect=ValueError("Shouldn't call bik verification")),
    )


@pytest.fixture
def always_passing_bik_verifier() -> BIKVerificationService:
    """Mock klasy odpowiedzialnej za komunikację z BIK.

    Zawsze zwraca pozytywną weryfikację (dana osoba nie jest oszustem)."""

    def passing_verify(customer: Customer) -> CustomerVerificationResult:
        return CustomerVerificationResult.create_passed(customer.uuid)

    return Mock(spec_set=BIKVerificationService, verify=passing_verify)
