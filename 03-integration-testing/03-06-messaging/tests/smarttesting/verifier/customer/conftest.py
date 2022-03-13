import socket
from time import sleep
from typing import Generator

import docker
import pytest
from docker.models.containers import Container
from kombu import Connection


@pytest.fixture
def random_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    _address, number = sock.getsockname()
    sock.close()
    return number


@pytest.fixture
def rabbitmq(  # pylint: disable=redefined-outer-name
    random_port: int,
) -> Generator[str, None, None]:
    """Fikstura startująca w tle kontener z RabbitMQ na losowym porcie.

    Zwraca DSN, który można wykorzystać do ustawienia połączenia w SQLAlchemy.
    """
    client = docker.from_env()
    db_container: Container = client.containers.run(
        "rabbitmq:3.7",
        detach=True,
        ports={
            5672: random_port,
        },
        environment={
            "RABBITMQ_DEFAULT_USER": "smarttesting",
            "RABBITMQ_DEFAULT_PASS": "pwd",
            "RABBITMQ_DEFAULT_VHOST": "test",
        },
    )
    broker_url = f"amqp://smarttesting:pwd@localhost:{random_port}/test"
    try:
        _wait_until_broker_is_ready(broker_url)
        yield broker_url
    finally:
        db_container.remove(force=True)


def _wait_until_broker_is_ready(url: str) -> None:
    """Oczekiwanie przez maksymalnie 10 sekund aż broker będzie gotowy."""
    for _ in range(50):
        try:
            Connection(url, connect_timeout=1).connect()
        except IOError:
            sleep(0.1)
            continue
        else:
            return

    raise TimeoutError("Test broker was not ready in time!")
