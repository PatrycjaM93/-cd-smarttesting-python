from smarttesting.customer.person import Person


class VerifierManager:
    """Klasa udająca klasę, która robi zdecydowanie za dużo."""

    def verify_tax_information(  # pylint: disable=unused-argument
        self, person: Person
    ) -> bool:
        return True

    def verify_address(self, person: Person) -> bool:  # pylint: disable=unused-argument
        return True

    def verify_name(self, person: Person) -> bool:  # pylint: disable=unused-argument
        return True

    def verify_surname(self, person: Person) -> bool:  # pylint: disable=unused-argument
        return True

    def verify_phone(self, person: Person) -> bool:  # pylint: disable=unused-argument
        return True
