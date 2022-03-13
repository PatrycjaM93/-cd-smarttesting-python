import logging
from typing import Any, Type, TypeVar

from fastapi import Depends, FastAPI, Request, Response, status
from smarttesting.client.customer_verification_result import Status
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Person

logger = logging.getLogger(__name__)


app = FastAPI()


TypeToInject = TypeVar("TypeToInject")


def Injects(item: Type[TypeToInject]) -> TypeToInject:  # pylint: disable=invalid-name
    """Minimalna integracja FastAPI z Injectorem.

    Zapewnia nam wstrzykiwanie pożądanych obiektów do widoku o ile "otoczymy" je
    wywołaniem Injects(DesiredClass), analogicznie jak wbudowany w FastAPI Depends.
    """

    def inject(request: Request) -> Any:
        return request.app.state.injector.get(item)

    return Depends(inject)


@app.post("/fraudCheck", status_code=status.HTTP_200_OK)
def fraud_check_view(
    person: Person,
    response: Response,
    customer_verifier=Injects(CustomerVerifier),
):
    """
    Widok dla żądania sprawdzenia potencjalnego fraudu.

    Zwraca status 200 dla osoby uczciwej, 401 dla oszusta.
    """
    logger.info("Received a verification request for person %s", person)
    result = customer_verifier.verify(person)
    if result.status == Status.VERIFICATION_FAILED:
        response.status_code = status.HTTP_401_UNAUTHORIZED
