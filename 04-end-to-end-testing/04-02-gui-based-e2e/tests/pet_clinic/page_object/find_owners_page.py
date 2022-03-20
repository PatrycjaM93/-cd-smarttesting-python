from selenium.webdriver.common.by import By
from tests.pet_clinic.page_object.add_owner_page import AddOwnerPage
from tests.pet_clinic.page_object.page_element import PageElement
from tests.pet_clinic.page_object.page_object import PageObject


class FindOwnersPage(PageObject):

    _add_owner_submit = PageElement((By.LINK_TEXT, "REGISTER"))

    def navigate_to_add_owner(self) -> AddOwnerPage:
        self._add_owner_submit.click()
        return AddOwnerPage(self.driver)
