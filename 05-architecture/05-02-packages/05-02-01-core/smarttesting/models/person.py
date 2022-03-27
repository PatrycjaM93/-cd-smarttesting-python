from dataclasses import dataclass
from typing import Optional

from smarttesting.tasks import send_email
from smarttesting.taxes import TaxService


@dataclass
class Person:
    """Klasa udająca, że jest modelem Active Record (np. Django ORM)."""

    person_id: int
    name: str
    surname: str
    dues: Optional[int] = 0

    def calculate(self) -> None:
        tax = TaxService()
        self.dues = tax.calculate()
        send_email.delay(person_id=self.person_id, dues=self.dues)
        self.save()

    def save(self) -> None:
        """Active Record ORM by to miał!"""
