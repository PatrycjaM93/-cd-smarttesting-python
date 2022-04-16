from dataclasses import dataclass

from smarttesting.verifier.application.event import Event


@dataclass(frozen=True)
class VerificationEvent(Event):
    """Zdarzenie związane z weryfikacją klienta."""

    source_description: str
    verification_successful: bool
