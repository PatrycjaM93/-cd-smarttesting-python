import uuid

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser


class FraudUser(FastHttpUser):
    wait_time = between(1, 2)
    connection_timeout = 1

    def on_start(self):
        """Tu może być kod do wykonania przed testem.

        Przykładowo, mógłoby to być uderzenie na endpoint logowania.
        W tym przykładzie nie ma jednak takiej potrzeby.
        """

    @task
    def perform_fraud_check(self):
        current_uuid = str(uuid.uuid4())
        payload = {
            "uuid": current_uuid,
            "person": {
                "name": "Jan",
                "surname": f"Fraudowski_{current_uuid}",
                "date_of_birth": "1980-01-01",
                "gender": "MALE",
                "national_id_number": "2345678901",
            },
        }
        with self.client.post(
            "/fraudCheck", json=payload, catch_response=True
        ) as response:
            # Domyślnie locust potraktuje odpowiedzi o kodzie 401 jak błędy
            # Chcemy by uznawał je za sukces, gdyż u nas to normalny wynik oznaczający
            # nieprzejście weryfikacji
            if response.status_code == 401:
                response.success()
