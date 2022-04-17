from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationResult:
    verification_name: str
    result: bool
