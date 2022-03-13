# pylint: disable=redefined-outer-name
import socket
from datetime import date
from multiprocessing import Process
from time import sleep
from typing import Generator

import pytest
import uvicorn


@pytest.fixture(scope="module")
def random_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    _address, number = sock.getsockname()
    sock.close()
    return number


@pytest.fixture(scope="module")
def root_address(random_port: int) -> str:
    """Prosta fikstura doklejająca losowo wybrany, wolny port do adresu localhost."""
    return f"http://127.0.0.1:{random_port}/"


@pytest.fixture(scope="module")
def app_path() -> str:
    return "smarttesting.client.app:app"


@pytest.fixture(scope="module")
def running_server(random_port: int, app_path: str) -> Generator:
    """Fikstura uruchamiająca proces w tle w osobnym procesie.

    Słowo kluczowe `yield` w drugiej od dołu linii powoduje przerwanie wykonania
    i powrót do fikstury na koniec testów w tym module (scope="module").
    Dzięki temu mamy okazję posprzątać, chociaż flaga daemon=True spowodowałaby że
    system operacyjny ubiłby proces po tym jak ten pytesta się zakończy.
    """
    host = "127.0.0.1"
    server_process = Process(
        target=uvicorn.run,
        args=(app_path,),
        kwargs={"host": host, "port": random_port},
        daemon=True,
    )
    server_process.start()
    _wait_until_server_is_ready(host, random_port)
    yield
    server_process.terminate()


def _wait_until_server_is_ready(host: str, port: int) -> None:
    """Oczekiwanie przez maksymalnie 5 sekund aż serwer będzie gotowy."""
    for _ in range(25):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
        except ConnectionRefusedError:
            sleep(0.1)
            continue
        else:
            return

    raise TimeoutError("Test server was not ready in time!")


@pytest.fixture()
def current_date_formatted() -> str:
    return date.today().strftime("%Y-%m-%d")
