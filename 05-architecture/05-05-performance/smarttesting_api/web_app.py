"""Prosta, demonstracyjna aplikacja flaskowa."""
import os
from http import HTTPStatus

import marshmallow
import marshmallow_dataclass
from flask import Flask, Response, jsonify, request
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from marshmallow import ValidationError
from marshmallow.fields import Field
from sqlalchemy.orm import Session

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting_main.smart_testing_application import assemble

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
    if result.passed:
        return jsonify({"message": "Weryfikacja udana"})
    else:
        return jsonify({"message": "Bagiety już jadą"}), HTTPStatus.UNAUTHORIZED


APP_ENV = "DEV" if DEV_MODE else "PROD"
app_injector = assemble(env=APP_ENV)  # type: ignore
FlaskInjector(app=app, injector=app_injector)
