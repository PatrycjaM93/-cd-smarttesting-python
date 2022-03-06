import abc

from smarttesting.customer.person import Person


class Verification(abc.ABC):
    """Weryfikacja klienta."""

    @abc.abstractmethod
    def passes(self, person: Person) -> bool:
        """Weryfikuje czy dana osoba nie jest oszustem."""
        pass  # pylint: disable=unnecessary-pass
