import os
from typing import Literal, cast

from flask import Flask
from flask_injector import FlaskInjector
from smarttesting.bik.web.main import assemble
from smarttesting.bik.web.views.score import score

DEV_MODE = False
if os.environ.get("APP_ENV") == "DEV":
    os.environ["FLASK_ENV"] = "development"
    DEV_MODE = True

APP_ENV = cast(Literal["DEV", "PROD"], "DEV" if DEV_MODE else "PROD")

app = Flask(__name__)
app.add_url_rule("/<pesel>", view_func=score)
FlaskInjector(app=app, injector=assemble(env=APP_ENV))
