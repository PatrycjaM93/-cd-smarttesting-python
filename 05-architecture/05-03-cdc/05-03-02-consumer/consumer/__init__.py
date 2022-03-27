import json
from datetime import date
from http import HTTPStatus
from typing import Any, TypedDict
from uuid import UUID

import requests

FRAUD_CHECK_URL = "http://localhost:5001/fraudCheck"


class PersonPayload(TypedDict):
    name: str
    surname: str
    national_id_number: str
    gender: str
    date_of_birth: date


class CustomerCheckPayload(TypedDict):
    uuid: UUID
    person: PersonPayload


def check_customer(payload: CustomerCheckPayload) -> bool:
    response = requests.post(
        FRAUD_CHECK_URL,
        data=json.dumps(payload, cls=CustomJSONEncoder),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == HTTPStatus.OK:
        return True
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        return False
    else:
        raise ValueError(
            f"Unexpected response code from fraud service - {response.status_code}"
        )


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)
