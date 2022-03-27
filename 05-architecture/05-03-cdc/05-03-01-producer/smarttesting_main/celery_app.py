import os

from celery import Celery
from smarttesting_main.smart_testing_application import assemble

env = os.environ.get("APP_ENV", "DEV")
app_injector = assemble(env=env)  # type: ignore

app = app_injector.get(Celery)
