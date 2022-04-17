import logging
from dataclasses import dataclass, field
from queue import Queue
from typing import List

from smarttesting.verifier.application.verification_event import VerificationEvent

logger = logging.getLogger(__name__)


@dataclass
class VerificationListener:
    """Nasłuchiwacz na zdarzenia weryfikacyjne. Zapisuje je w kolejce."""

    _queue: Queue = field(default_factory=Queue)
    _events: List[VerificationEvent] = field(default_factory=list)

    def receive(self, event: VerificationEvent) -> None:
        logger.info("Got an event! %s", event)
        self._queue.put(event)

    def _drain(self) -> None:
        """Pobierz nowe eventy i doczep je do listy w pamięci."""
        for _ in range(self._queue.qsize()):
            event = self._queue.get_nowait()
            self._events.append(event)

    @property
    def received_events(self) -> List[VerificationEvent]:
        self._drain()
        return self._events[:]
