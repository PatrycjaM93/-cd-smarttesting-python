from dataclasses import dataclass
from typing import Dict, List, Protocol, Type

from smarttesting.verifier.application.event import Event


class Listener(Protocol):
    def receive(self, event: Event) -> None:
        ...


@dataclass
class EventBus:
    """Prosta implementacja event busa in-memory."""

    _subscriptions: Dict[Type[Event], List[Listener]]

    def publish(self, event: Event) -> None:
        for listener in self._subscriptions.get(type(event), []):
            listener.receive(event)

    def __hash__(self) -> int:
        return id(self)
