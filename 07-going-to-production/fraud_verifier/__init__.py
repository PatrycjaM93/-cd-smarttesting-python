import os
import pathlib
from http import HTTPStatus

import injector
from flask import Flask, jsonify, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from flask_zipkin import Zipkin
from marshmallow import ValidationError
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from fraud_verifier.customer.customer_verifier import CustomerVerifier
from fraud_verifier.feature_toggles.features import Feature
from fraud_verifier.feature_toggles.model import Base, FeatureModel
from fraud_verifier.modules.db import DbModule
from fraud_verifier.modules.feature_toggles import FeatureTogglesModule
from fraud_verifier.modules.fraud_verifier import FraudVerifierModule
from fraud_verifier.schemas import CustomerSchema, CustomerVerificationResultSchema

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


SQLITE_PATH = str(pathlib.Path(__file__).parent / "db.sqlite")

container = injector.Injector(
    [DbModule(SQLITE_PATH), FeatureTogglesModule(), FraudVerifierModule()]
)
FlaskInjector(app, injector=container)
Zipkin(app, sample_rate=100)
PrometheusMetrics(app)
app.config["ZIPKIN_DSN"] = "http://zipkin:9411/api/v1/spans"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["SECRET_KEY"] = "extra-secret"
admin = Admin(app, name=__name__, template_mode="bootstrap4")
admin.add_view(ModelView(FeatureModel, container.get(Session)))


@app.before_first_request
def prepare_app():
    # Recreate file-based Sqlite database
    try:
        os.remove(SQLITE_PATH)
    except FileNotFoundError:
        pass  # it's ok, will be created
    engine = container.get(Engine)
    Base.metadata.create_all(engine)

    session = container.get(Session)
    session.add(FeatureModel(name=Feature.NEW_VERIFICATION.name, enabled=False))
    session.commit()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9090)
