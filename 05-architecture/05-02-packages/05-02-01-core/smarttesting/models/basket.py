"""Jako ilustracja do _02_threadlocals_tests.

Antyprzykład wykorzystania threadlocals - klasy Basket nawet nie da się przetestować
bez podniesienia całego kontekstu aplikacji Flaska lub zamockowania tejże.
"""
from dataclasses import dataclass, field
from typing import Dict

from flask import request


@dataclass
class Basket:
    user_id: int
    items: Dict[int, int] = field(default_factory=dict)

    @classmethod
    def get_from_request(cls) -> "Basket":
        basket_id = request.cookies.get("basket-id")
        if basket_id is None:
            return Basket(0, {})
        else:
            # pobierz z bazy po id, cokolwiek innego
            return Basket(1, {})
