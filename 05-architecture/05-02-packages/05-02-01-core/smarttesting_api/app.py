from flask import Flask, jsonify
from smarttesting.models.basket import Basket

app = Flask(__name__)


@app.route("/baskets")
def current_basket():
    basket = Basket.get_from_request()
    return jsonify({"user_id": basket.user_id, "items": basket.items})
