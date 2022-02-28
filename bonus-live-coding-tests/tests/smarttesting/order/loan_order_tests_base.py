import logging
from datetime import date
from typing import ClassVar
from uuid import uuid4

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person


class LoanOrderTestsBase:
    """Bazowa klasa testowa, z której dziedziczą klasy testowe w pakiecie.

    Jest to jedno z możliwych rozwiązaniach uwspólniania wspólnego setupu.
    Alternatywnie możemy wykorzystać conftest.py obsługiwany przez pytesta.
    """

    logger: ClassVar = logging.getLogger("loan_order_tests")

    @pytest.fixture()
    def student(self) -> Customer:
        person = Person("Jan", "Nowicki", date(1996, 8, 28), Gender.MALE, "96082812079")
        customer = Customer(uuid4(), person)
        customer.student()
        return customer

    @pytest.fixture()
    def customer(self) -> Customer:
        person = Person(
            "Maria", "Kowalska", date(1989, 3, 10), Gender.FEMALE, "89031013409"
        )
        return Customer(uuid4(), person)
