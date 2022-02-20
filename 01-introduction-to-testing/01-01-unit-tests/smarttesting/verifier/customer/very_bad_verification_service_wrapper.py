from smarttesting.verifier.customer.very_bad_verification_service import (
    VeryBadVerificationService,
)


class VeryBadVerificationServiceWrapper:
    """Klasa "wrapper" otaczająca statyczną metodę innej klasy.

    Statyczna metoda realizuje jakieś ciężkie operacje bazodanowe. Nie polecamy
    robienia czegoś takiego w metodzie statycznej, ale tu pokazujemy jak to obejść
    i przetestować jeżeli z jakiegoś powodu nie da się tego zmienić (np. metoda
    statyczna jest dostarczana przez kogoś innego).

    Jeżeli próbujemy przetestować coś, co używa takiego kodu to możemy mieć problem.
    Pozostaje sztuczka z podmianką (pokazywana testach) lub monkey-patching.
    """

    def verify(self) -> bool:
        return VeryBadVerificationService.run_heavy_queries_to_db()
