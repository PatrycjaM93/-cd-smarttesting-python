from smarttesting.verifier.application.verification_event import VerificationEvent
from smarttesting.verifier.customer.verification_listener import VerificationListener


class TestVerificationListener:
    def test_should_add_event(self) -> None:
        listener = VerificationListener()
        event = VerificationEvent(self, "age", True)

        listener.receive(event)

        assert listener.received_events == [event]
