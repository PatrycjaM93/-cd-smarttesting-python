import pytest
from flask import request as request_threadlocal_proxy
from smarttesting.models import basket


class Test02Threadlocals:
    """
    Wiele popularnych Pythonowych frameworków wykorzystuje mechanizm threadlocal
    aby rozwiązac problem przekazywania zależności. Z zewnątrz wygląda to jak zmienna
    globalna, którą importujemy i z niej korzystamy w kodzie. threadlocal gwarantuje,
    że w jednym wątku (najczęściej - tym samym requeście) będziemy dostawać dokładnie
    ten sam obiekt. Dobry przykład to flask.request, będący proxy-objectem na bieżący
    obiekt żądania.

    Utrzymywalność takich rozwiązań jest jednak mocno wątpliwa a i przetestowanie nie
    należy do najłatwiejszych - szczególnie, jeśli dana biblioteka nie udostępnia
    narzędzi do zarządzania stanem obiektów wykorzystywanych za pośrednictwem
    threadlocali (np. test clienta).

    Testy mogą potencjalnie zabezpieczyć nas przed złym wykorzystaniem threadlocali.
    Pomijając trudność wykonania (trzeba obsłużyć całkiem sporo przypadków), to chodzi
    tu bardziej o koncepcję i celowość takich testów - próbujemy za ich pomocą wymusić
    konwencje i dobre praktyki.
    """

    @pytest.mark.xfail()  # Ten test nie przechodzi bo ma demaskować źle napisany kod
    def test_request_proxy_not_in_module(self) -> None:
        """Próba wykrycia, czy ktoś nie próbuje importować threadlocala w kodzie.

        W Pythonie wszystko jest obiektem, także moduł. Jeżeli ktoś coś importuje,
        to ten obiekt jest dodawanay do __dict__ modułu pod zaimportowaną nazwą.

        W tym teście spróbujemy wykryć tylko jeden prosty przypadek:
        - czy ktoś nie importuje bezpośrednio `flask.request`
        """
        # Pobieramy atrybut o nazwie `request` modułu basket lub None
        # jeżeli w module basket zrobimy `from flask import request` to dokładnie
        # taki atrybut zostanie dodany do wspomnianego modułu
        request_in_basket = getattr(basket, "request", None)

        assert request_in_basket is not request_threadlocal_proxy

    @pytest.mark.xfail()  # Ten test nie przechodzi bo ma demaskować źle napisany kod
    def test_request_proxy_not_aliased_in_module(self) -> None:
        """Próba wykrycia, czy ktoś nie próbuje importować threadlocala w kodzie.

        Nieco sprytniejsze podejście niż poprzednio - tym razem wykryjemy także
        aliasowanie przechodząc po wszystkich rzeczach zaimportowanych i sprawdzając,
        czy któraś z nich przypadkiem nie znajduje się na liście "zakazanych" obiektów.
        """
        forbidden_objects = [request_threadlocal_proxy]
        for _attr_name, attr_value in vars(basket).items():
            for obj in forbidden_objects:
                assert attr_value is not obj
