from typing import Optional, Type

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tests.pet_clinic.page_object.page_object import PageObject


class PageElement:
    """Trochę pythonowej magii w służbie dobra - deskryptory!"""

    def __init__(self, locator: tuple) -> None:
        """Na przykład: PageElement(((By.LINK_TEXT, "REGISTER"))"""
        self._locator = locator

    def __get__(
        self, instance: PageObject, owner: Optional[Type[PageObject]]
    ) -> WebElement:
        return WebDriverWait(instance.driver, 20).until(
            EC.presence_of_element_located(self._locator)
        )
