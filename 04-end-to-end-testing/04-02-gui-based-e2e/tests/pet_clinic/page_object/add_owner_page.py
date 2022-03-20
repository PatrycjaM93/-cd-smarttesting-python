from selenium.webdriver.common.by import By
from tests.pet_clinic.page_object.owner_view_page import OwnerViewPage
from tests.pet_clinic.page_object.page_element import PageElement
from tests.pet_clinic.page_object.page_object import PageObject


class AddOwnerPage(PageObject):
    _first_name_input = PageElement((By.NAME, "firstName"))
    _last_name_input = PageElement((By.NAME, "lastName"))
    _address = PageElement((By.NAME, "address"))
    _city = PageElement((By.NAME, "city"))
    _telephone = PageElement((By.NAME, "telephone"))
    _add_owner_submit = PageElement((By.XPATH, "/html/body//owner-form//button"))

    def fill_first_name(self, first_name: str) -> None:
        self._first_name_input.send_keys(first_name)

    def fill_last_name(self, last_name: str) -> None:
        self._last_name_input.send_keys(last_name)

    def fill_address(self, address: str) -> None:
        self._address.send_keys(address)

    def fill_city(self, city: str) -> None:
        self._city.send_keys(city)

    def fill_telephone_number(self, telephone_number: str) -> None:
        self._telephone.send_keys(telephone_number)

    # Powtarzalne elementy w tej klasie, to jest metody fill_xxx, gdzie xxx to nazwa
    # pola można by "zautomatyzować" przez metodę __getattr__, jednak stracilibyśmy
    # wsparcie IDE, mypy i podpowiedzi

    def add_owner(self) -> OwnerViewPage:
        """Zwraca obiekt kolejnej strony."""
        self._add_owner_submit.click()
        return OwnerViewPage(self.driver)
