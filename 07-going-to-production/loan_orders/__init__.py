from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from flask_zipkin import Zipkin
from marshmallow import ValidationError
from prometheus_flask_exporter import PrometheusMetrics

from loan_orders.modules.loan_orders import LoanOrdersModule
from loan_orders.modules.persistence import PersistenceModule
from loan_orders.order.loan_order_service import LoanOrderService
from loan_orders.schemas import LoanOrderSchema

app = Flask(__name__)


@app.route("/orders", methods=["POST"])
@expects_json()
def create_order(service: LoanOrderService):
    try:
        loan_order = LoanOrderSchema().load(request.json)  # type: ignore
    except ValidationError as validation_error:
        return jsonify(validation_error.messages), HTTPStatus.BAD_REQUEST

    return service.verify_loan_order(loan_order)


@app.route("/orders/<order_id>")
def get_order(order_id: str, service: LoanOrderService):
    order = service.find_order(order_id)
    if order:
        schema = LoanOrderSchema()
        return schema.dump(order)
    else:
        return {"message": "Not found"}, 404


FlaskInjector(app, [LoanOrdersModule(), PersistenceModule()])
Zipkin(app, sample_rate=100)
PrometheusMetrics(app)
app.config["ZIPKIN_DSN"] = "http://zipkin:9411/api/v1/spans"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9091)
