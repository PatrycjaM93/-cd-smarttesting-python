from smarttesting.verifier.verification_event import VerificationEvent


class EventEmitter:
    """Klasa udająca klasę łączącą się po brokerze wiadomości."""

    def emit(self, event: VerificationEvent) -> None:
        pass
