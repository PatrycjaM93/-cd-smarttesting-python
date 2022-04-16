import logging
from typing import List, Optional

from fastapi import FastAPI
from injector import Injector, Module, provider
from smarttesting.client.age_verification import AgeVerification
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.fraud_view import app as vanilla_app


class FraudModule(Module):
    @provider
    def customer_verifier(self) -> CustomerVerifier:
        return CustomerVerifier({AgeVerification()})


def create_app(modules: Optional[List[Module]] = None) -> FastAPI:
    """Dla uruchamiania lokalnie/produkcyjnie z całym serwerem."""

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s:     %(asctime)s:%(message)s"
    )
    logging.getLogger("uvicorn").propagate = False

    if not modules:
        modules = [FraudModule()]
    vanilla_app.state.injector = Injector(modules)
    return vanilla_app


app = create_app()
