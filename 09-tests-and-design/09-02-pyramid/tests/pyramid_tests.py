# pylint: disable=unused-argument
"""Wyłączamy czujengo pylinta by nie oprotestowywał tego demonstracyjnego kodu."""
from dataclasses import dataclass

from flask import Flask

app = Flask(__name__)


@app.route("/users/<user_id>")
def user_view(repo: "UserRepository", user_id: str):
    user = repo.find_by_id(user_id)
    return serialize(user)


def serialize(user: "User") -> dict:
    return {}


class User:
    ...


class Dao:
    def execute_sql(self, sql: str) -> User:
        ...


class Repository:
    ...


@dataclass
class UserRepository(Repository):
    _dao: Dao

    def find_by_id(self, user_id: str) -> User:
        return self._dao.execute_sql("...")
