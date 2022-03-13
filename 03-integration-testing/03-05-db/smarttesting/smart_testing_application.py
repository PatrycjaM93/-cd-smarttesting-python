from injector import Injector
from smarttesting.verifier.customer.module import CustomerModule
from smarttesting.verifier.customer.verification.module import VerificationModule


def assemble() -> Injector:
    """Avengers! ...assemble! A nie, to tylko zainicjowanie kontenera IoC :)"""
    return Injector(
        modules=[
            VerificationModule(),
            CustomerModule(),
        ],
        auto_bind=False,
    )
