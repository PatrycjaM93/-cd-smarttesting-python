from typing import NewType

import injector
from celery import Celery
from kombu.serialization import register
from smarttesting import serialization

BrokerUrl = NewType("BrokerUrl", str)


class CeleryModule(injector.Module):
    def __init__(self, broker_url: str) -> None:
        self._broker_url = broker_url

        register(
            "dataclasses_serialization",
            serialization.dataclass_dump,
            serialization.dataclass_load,
            content_type="application/json",
            content_encoding="utf-8",
        )

    @injector.provider
    def broker_url(self) -> BrokerUrl:
        return BrokerUrl(self._broker_url)

    @injector.singleton
    @injector.provider
    def celery(self, broker_url: BrokerUrl, container: injector.Injector) -> Celery:
        app = Celery(broker=broker_url)
        app.__injector__ = container

        class CeleryConfig:
            accept_content = {"json", "dataclasses_serialization"}
            task_serializer = "dataclasses_serialization"
            result_backend = "rpc://"
            result_persistent = False

        app.config_from_object(CeleryConfig)
        return app
