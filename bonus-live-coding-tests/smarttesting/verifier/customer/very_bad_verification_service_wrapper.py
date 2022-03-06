from smarttesting.verifier.customer.very_bad_verification_service import (
    VeryBadVerificationService,
)


class VeryBadVerificationServiceWrapper:
    """Klasa "wrapper" otaczająca statyczną metodę.

    Statyczna metoda realizuje jakieś ciężkie operacje bazodanowe. Nie polecamy
    robienia czegoś takiego w metodzie statycznej, ale tu pokazujemy jak to obejść
    i przetestować jeżeli z jakiegoś powodu nie da się tego zmienić (np. metoda
    statyczna jest dostarczana przez kogoś innego).
    """

    def verify(self) -> bool:
        return VeryBadVerificationService.run_heavy_queries_to_db()
