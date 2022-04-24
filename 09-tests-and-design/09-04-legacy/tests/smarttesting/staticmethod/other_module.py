# pylint: disable=invalid-name,unused-argument
from tests.smarttesting.staticmethod.client import Client


class _19_DatabaseAccessor:
    def get_client_by_name(self, name: str) -> Client:
        client = self._perform_long_running_task(name)
        print(client.name)
        self._do_some_additional_work(client)
        return client

    def _perform_long_running_task(self, name: str) -> Client:
        raise IOError("Can't connect to the database!")

    def _do_some_additional_work(self, client: Client) -> None:
        print("Additional work done")


# Tak można mieć singleton w Pythonie 8)
database_accessor = _19_DatabaseAccessor()
