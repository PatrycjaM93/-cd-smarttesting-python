from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationEvent:
    passed: bool
