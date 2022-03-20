from selenium.webdriver.common.by import By
from tests.pet_clinic.page_object.find_owners_page import FindOwnersPage
from tests.pet_clinic.page_object.page_element import PageElement
from tests.pet_clinic.page_object.page_object import PageObject


class HomePage(PageObject):
    _owners_link = PageElement((By.LINK_TEXT, "OWNERS"))

    def navigate_to_find_owners(self) -> FindOwnersPage:
        self._owners_link.click()
        return FindOwnersPage(self.driver)
