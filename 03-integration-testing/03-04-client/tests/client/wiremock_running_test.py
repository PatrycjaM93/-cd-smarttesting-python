import os

import pytest
import requests
from requests.exceptions import RequestException
from wiremock.constants import Config


@pytest.mark.wiremock()
class WiremockRunningTest:
    """
    Klasa bazowa ułatwiająca pisanie testów korzystających z wiremocka.
    """

    WIREMOCK_PORT = 8080
    WIREMOCK_HOST = os.environ.get("WIREMOCK_HOST", "localhost")  # for CI
    ADMIN_PATH = f"http://{WIREMOCK_HOST}:{WIREMOCK_PORT}/__admin/"

    @pytest.fixture(scope="class", autouse=True)
    def start_stop_wiremock(self):
        """
        Ta fikstura ma zapewniać uruchamianie świeżej instancji serwera wiremock
        na każdą klasę testową.

        Pythonowy klient wiremocka posiada błąd, przez który nie działa uruchamianie
        samego wiremocka w tle. Dopóki nie zostanie załatany, ta fikstura upewnia się
        tylko że serwer jest osiągalny i działa pod zadanym portem.

        Zobacz: https://github.com/platinummonkey/python-wiremock/issues/31
        """
        try:
            response = requests.get(self.ADMIN_PATH)
            response.raise_for_status()
        except RequestException:
            pytest.fail(
                f"Musisz uruchomić serwer wiremocka na porcie {self.WIREMOCK_PORT}, "
                f"np. `docker run -it --rm -p {self.WIREMOCK_PORT}:8080 "
                f"rodolpheche/wiremock:2.27.2\nWięcej informacji o usłudze: "
                "http://wiremock.org/docs/running-standalone/"
            )
        else:
            Config.base_url = (
                f"http://{self.WIREMOCK_HOST}:{self.WIREMOCK_PORT}/__admin"
            )
