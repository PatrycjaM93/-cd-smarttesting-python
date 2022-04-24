from smarttesting.customer.person import Person


class SurnameChecker:
    """Klasa udająca, że weryfikuje osobę po nazwisku."""

    def check_surname(self, person: Person) -> bool:  # pylint: disable=unused-argument
        return False
