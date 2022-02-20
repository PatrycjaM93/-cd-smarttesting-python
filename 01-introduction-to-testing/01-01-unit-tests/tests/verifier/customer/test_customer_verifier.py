import uuid
from datetime import date
from typing import Set
from unittest import mock

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
    Status,
)
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.simple_verification import SimpleVerification
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.customer.very_bad_verification_service_wrapper import (
    VeryBadVerificationServiceWrapper,
)
from smarttesting.verifier.verification import Verification


class StubVerificationService(BIKVerificationService):
    """Implementacja testowa (Test Double).

    W celu uniknięcia kontaktowania się z zewnętrznym serwisem w testach jednostkowych.
    """

    def __init__(self) -> None:
        super().__init__("http://example.com")

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        return CustomerVerificationResult.create_passed(customer.uuid)


class TestBadServiceWrapper(VeryBadVerificationServiceWrapper):
    """Implementacja testowa (Test Double).

    W celu uniknięcia kontaktowania się z zewnętrznym serwisem w testach jednostkowych.
    """

    def verify(self) -> bool:
        return True


class TestCustomerVerifier:
    """
    Klasa zawiera przykłady inicjalizacji w polach testowych, przykład false passes,
    przykład zastosowania Test Doubles.

    Zestaw testów zawiera test na przypadek negatywny `test_fails_simple_verification`,
    ale nie zawiera tesów weryfikujących pozytywną weryfikację, przez co testy nie
    wychwytują, że kod produkcyjny zwraca domyślną wartość i brakuje implementacji
    logiki biznesowej.
    """

    def test_verifies_person(self) -> None:
        # Given
        customer = self._build_customer()
        service = CustomerVerifier(
            StubVerificationService(),
            self._build_verifications(),
            TestBadServiceWrapper(),
        )

        # When
        result = service.verify(customer)

        # Then
        assert result.status == Status.VERIFICATION_PASSED
        assert result.user_id == customer.uuid

    def _build_verifications(self) -> Set[Verification]:
        return {
            AgeVerification(),
            IdentificationNumberVerification(),
        }

    def test_fails_simple_verification(self) -> None:
        """Test weryfikuje przypadek negatywnej weryfikacji, ale w klasie zabrakło
        testu na pozytywną weryfikację klienta. Przez to testy nie wychwytują, że kod
        produkcyjny zwraca domyślną wartość i brakuje implementacji logiki biznesowej.
        """
        # Given
        customer = self._build_customer()
        service = CustomerVerifier(
            StubVerificationService(),
            self._build_simple_verifications(),
            TestBadServiceWrapper(),
        )

        # When
        result = service.verify(customer)

        # Then
        assert result.status == Status.VERIFICATION_FAILED

    def _build_simple_verifications(self) -> Set[Verification]:
        return {SimpleVerification()}

    def _build_customer(self) -> Customer:
        person = Person("John", "Smith", date(1996, 8, 28), Gender.MALE, "96082812079")
        return Customer(uuid.uuid4(), person)

    def test_verifies_person_with_monkey_patching(self) -> None:
        """W tym teście użyjemy patchowania do porawdzenia sobie z zależnością, którą
        niełatwo będzie nam kontrolować w teście.

        W tym przypadku `CustomerVerifier` korzysta z
        `VeryBadVerificationServiceWrapper`, która to klasa bezpośrednio importuje
        inną klasę (nie dostaje go w __init__) i wywołuje na nim metodę statyczną.

        Nie zapominajmy, że monkey-patching powinien nam służyć jako ostateczność,
        nie domyslna strategia usuwania kłopotliwych zależności.
        """
        # Given
        customer = self._build_customer()
        service = CustomerVerifier(
            StubVerificationService(),
            self._build_verifications(),
            # używamy oryginalnej, problematycznej implementacji...
            VeryBadVerificationServiceWrapper(),
        )

        # When
        # ...by ją podmienić na czas samego działania:
        to_patch = (
            "smarttesting.verifier.customer.very_bad_verification_service_wrapper."
            "VeryBadVerificationServiceWrapper.verify"
        )
        with mock.patch(to_patch, return_value=True):
            result = service.verify(customer)

        # Then
        assert result.status == Status.VERIFICATION_PASSED
        assert result.user_id == customer.uuid
