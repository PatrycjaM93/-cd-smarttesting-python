# pylint: disable=redefined-outer-name
import random
import time
import uuid
from http import HTTPStatus
from typing import Generator
from unittest import mock

import pytest
from flask.testing import FlaskClient
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting_api import web_app
from sqlalchemy.exc import OperationalError


@pytest.fixture()
def test_client() -> Generator[FlaskClient, None, None]:
    with web_app.app.test_client() as client:
        yield client


@pytest.fixture()
def fraud_payload() -> dict:
    return {
        "uuid": str(uuid.uuid4()),
        "person": {
            "date_of_birth": "2020-01-01",
            "gender": "FEMALE",
            "name": "Stefania",
            "national_id_number": "1234567890",
            "surname": "Stefanowska",
        },
    }


@pytest.mark.xfail
def test_returns_401_within_500_ms_when_calling_fraud_check_with_introduced_latency(
    test_client: FlaskClient,
    fraud_payload: dict,
) -> None:
    """
    Hipoteza stanu ustalonego
        POST na URL “/fraudCheck”,
        reprezentujący oszusta,
        odpowie statusem 401w ciągu 500 ms
    Metoda
        Włączamy opóźnienie mające miejsce w kliencie BIK używając monkey-patchingu
    Wycofanie
        Wycofujemy monkey-patching
    """
    sleep_for = random.randint(1000, 3000) / 1000

    original_method = BIKVerificationService.verify

    def take_your_time_verifying_national_id_no(*args, **kwargs):
        time.sleep(sleep_for)
        result = original_method(*args, **kwargs)
        return result

    to_patch = (
        "smarttesting.verifier.customer.bik_verification_service."
        "BIKVerificationService.verify"
    )
    with mock.patch(to_patch, take_your_time_verifying_national_id_no):
        start = time.time()
        response = test_client.post("/fraudCheck", json=fraud_payload)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    lasted = time.time() - start
    assert lasted <= 0.5, "Odpowiedź nie została zwrócona w 500ms!"


@pytest.mark.xfail
def test_returns_401_within_500ms_when_calling_fraud_check_with_db_issues(
    test_client: FlaskClient,
    fraud_payload: dict,
) -> None:
    """
    Hipoteza stanu ustalonego
        POST na URL “/fraudCheck”,
        reprezentujący oszusta,
        odpowie statusem 401w ciągu 500 ms
    Metoda
        Używając monkey-patching zasymulujemy błędy z bazą danych
    Wycofanie
        Wycofujemy monkey-patching
    """
    operational_error = OperationalError("", (), Exception())
    with mock.patch("sqlalchemy.orm.query.Query.first", side_effect=operational_error):
        start = time.time()
        response = test_client.post("/fraudCheck", json=fraud_payload)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    lasted = time.time() - start
    assert lasted <= 0.5, "Odpowiedź nie została zwrócona w 500ms!"
