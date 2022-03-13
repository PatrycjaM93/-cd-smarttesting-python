# pylint: disable=redefined-outer-name
import pytest
from smarttesting.client.customer_verifier import (
    AgeVerification,
    CustomerVerifier,
    Dao,
    EventEmitter,
    HttpCallMaker,
    IdentificationNumberVerification,
    NameVerification,
)


@pytest.fixture()
def customer_verifier(
    age_verification: AgeVerification,
    id_verification: IdentificationNumberVerification,
    name_verification: NameVerification,
) -> CustomerVerifier:
    return CustomerVerifier(age_verification, id_verification, name_verification)


@pytest.fixture()
def age_verification(http_call_maker: HttpCallMaker, dao: Dao) -> AgeVerification:
    return AgeVerification(http_call_maker, dao)


@pytest.fixture()
def id_verification(dao: Dao) -> IdentificationNumberVerification:
    return IdentificationNumberVerification(dao)


@pytest.fixture()
def name_verification(event_emitter: EventEmitter) -> NameVerification:
    return NameVerification(event_emitter)


@pytest.fixture()
def http_call_maker() -> HttpCallMaker:
    return HttpCallMaker()


@pytest.fixture()
def dao() -> Dao:
    return Dao()


@pytest.fixture()
def event_emitter() -> EventEmitter:
    return EventEmitter()
