from smarttesting.event.event import Event


class EventEmitter:
    """Klasa udająca klasę łączącą się po brokerze wiadomości."""

    def emit(self, event: Event) -> None:
        pass
