from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from fraud_verifier.customer.customer_verifier import CustomerVerifier
from fraud_verifier.modules.fraud_verifier import FraudVerifierModule
from fraud_verifier.schemas import CustomerSchema, CustomerVerificationResultSchema
from marshmallow import ValidationError

app = Flask(__name__)


@app.route("/customers/verify", methods=["POST"])
@expects_json()
def verify(verifier: CustomerVerifier):
    try:
        customer = CustomerSchema().load(request.json)  # type: ignore
    except ValidationError as validation_error:
        return jsonify(validation_error.messages), HTTPStatus.BAD_REQUEST

    result = verifier.verify(customer)
    result_schema = CustomerVerificationResultSchema()
    return result_schema.dump(result)


FlaskInjector(app, modules=[FraudVerifierModule()])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9090)
