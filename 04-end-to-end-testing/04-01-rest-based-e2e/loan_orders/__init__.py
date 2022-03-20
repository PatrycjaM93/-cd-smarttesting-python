from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from flask_injector import FlaskInjector
from loan_orders.modules.loan_orders import LoanOrdersModule
from loan_orders.modules.persistence import PersistenceModule
from loan_orders.order.loan_order_service import LoanOrderService
from loan_orders.schemas import LoanOrderSchema
from marshmallow import ValidationError

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
        data = schema.dump(order)
        data["customer"].pop("id")
        return data
    else:
        return {"message": "Not found"}, 404


FlaskInjector(app, [LoanOrdersModule(), PersistenceModule()])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9091)
