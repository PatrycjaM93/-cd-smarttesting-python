from dataclasses import dataclass
from uuid import UUID

from smarttesting.event.event import Event


@dataclass(frozen=True)
class LoanCreatedEvent(Event):
    _uuid: UUID

    @property
    def uuid(self) -> UUID:
        return self._uuid
