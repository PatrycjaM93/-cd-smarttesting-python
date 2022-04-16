# pylint: disable=redefined-outer-name
import uuid
from datetime import date
from typing import Set, cast

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.application.event_bus import EventBus, Listener
from smarttesting.verifier.application.verification_event import VerificationEvent
from smarttesting.verifier.customer._01_customer_verifier import CustomerVerifier
from smarttesting.verifier.customer._03_verification_listener import (
    VerificationListener,
)
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.verification import Verification


@pytest.fixture()
def verifications_listener() -> VerificationListener:
    return VerificationListener()


@pytest.fixture()
def publisher(verifications_listener: VerificationListener) -> EventBus:
    listener = cast(Listener, verifications_listener)
    return EventBus({VerificationEvent: [listener]})


@pytest.fixture()
def verifications(publisher: EventBus) -> Set[Verification]:
    return {
        AgeVerification(publisher),
        IdentificationNumberVerification(publisher),
        NameVerification(publisher),
    }


@pytest.fixture()
def verifier(verifications: Set[Verification]) -> CustomerVerifier:
    return CustomerVerifier(
        _verifications=verifications,
        _fraud_alert_task=None,
    )


@pytest.fixture()
def stefan() -> Customer:
    return Customer(
        _uuid=uuid.uuid4(),
        _person=Person(
            _name="",
            _surname="",
            _date_of_birth=date.today(),
            _gender=Gender.MALE,
            _national_id_number="0123456789",
        ),
    )
