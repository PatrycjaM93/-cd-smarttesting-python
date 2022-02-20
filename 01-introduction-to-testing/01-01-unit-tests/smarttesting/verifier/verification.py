import abc

from smarttesting.customer.person import Person


class Verification(abc.ABC):
    @abc.abstractmethod
    def passes(self, person: Person) -> bool:
        pass
