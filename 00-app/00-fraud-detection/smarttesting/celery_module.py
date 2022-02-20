from typing import NewType

import injector
from celery import Celery
from kombu.serialization import register

from smarttesting import serialization

CeleryConfig = NewType("CeleryConfig", object)


class CeleryModule(injector.Module):
    def __init__(self) -> None:
        register(
            "dataclasses_serialization",
            serialization.dataclass_dump,
            serialization.dataclass_load,
            content_type="application/json",
            content_encoding="utf-8",
        )

    @injector.singleton
    @injector.provider
    def celery(self, container: injector.Injector, config: CeleryConfig) -> Celery:
        app = Celery(config_source=config)
        app.__injector__ = container
        return app
