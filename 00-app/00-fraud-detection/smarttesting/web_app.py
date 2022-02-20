"""Prosta, demonstracyjna aplikacja flaskowa."""
import logging
import os
from http import HTTPStatus

import kombu
import marshmallow
import marshmallow_dataclass
from flask import Flask, Response, jsonify, request
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from marshmallow import ValidationError
from marshmallow.fields import Field
from sqlalchemy.orm import Session

from smarttesting.celery_module import CeleryConfig
from smarttesting.customer.customer import Customer
from smarttesting.fraud_detection_application import assemble
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier


logger = logging.getLogger(__name__)


DEV_MODE = False
if os.environ.get("APP_ENV") == "DEV":
    os.environ["FLASK_ENV"] = "development"
    DEV_MODE = True


app = Flask(__name__)


@app.after_request  # type: ignore
def close_tx(response: Response, session: Session) -> Response:
    session.commit()
    session.close()
    return response


class PrivateFieldsCapableSchema(marshmallow.Schema):
    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        # Dataclasses (w przeciwieństwie do attrs) nie aliasują prywatnych pól
        # w __init__, więc żeby API nie wymagało podawania pól w formacie "_uuid",
        # aliasujemy je usuwając podkreślnik
        field_obj.data_key = field_name.lstrip("_")


CustomerSchema = marshmallow_dataclass.class_schema(
    Customer, base_schema=PrivateFieldsCapableSchema
)


@app.route("/fraudCheck", methods=["POST"])
@expects_json()
def fraud_check(verifier: CustomerVerifier):
    try:
        customer = CustomerSchema().load(request.json)  # type: ignore
    except ValidationError as validation_error:
        return jsonify(validation_error.messages), HTTPStatus.BAD_REQUEST

    result = verifier.verify(customer=customer)
    logger.info("Verification for customer %r is %s", customer, result)
    if result.passed:
        return jsonify({"message": "Weryfikacja udana"})
    else:
        return jsonify({"message": "Bagiety już jadą"}), HTTPStatus.UNAUTHORIZED


@app.route("/health")
def health(session: Session, celery_config: CeleryConfig):
    try:
        session.execute("SELECT 1")
    except IOError:
        db_healthy = False
    else:
        db_healthy = True

    try:
        kombu.Connection(celery_config.broker_url).connect()  # type: ignore
    except IOError:
        broker_healthy = False
    else:
        broker_healthy = True

    response = {"health": {"db": db_healthy, "broker": broker_healthy}}
    if all([db_healthy, broker_healthy]):
        return response
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


APP_ENV = "DEV" if DEV_MODE else "PROD"
FlaskInjector(app=app, injector=assemble(env=APP_ENV))  # type: ignore
