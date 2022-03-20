import pytest
from faker import Faker
from selenium import webdriver
from tests.pet_clinic.page_object.add_owner_page import AddOwnerPage
from tests.pet_clinic.page_object.home_page import HomePage


class TestPetClinicPageObject:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.faker = Faker()
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8080")

        self.home_page = HomePage(self.driver)

        yield
        self.driver.quit()

    def test_adding_owner(self) -> None:
        """Test z wykorzystaniem Selenium Page Object pattern."""
        find_owners_page = self.home_page.navigate_to_find_owners()
        add_owner_page = find_owners_page.navigate_to_add_owner()
        first_name, last_name = self.faker.first_name(), self.faker.last_name()
        self._fill_owner_data(add_owner_page, first_name, last_name)

        owner_view_page = add_owner_page.add_owner()

        full_name = f"{first_name} {last_name}"
        assert owner_view_page.contains_text(full_name)

    def _fill_owner_data(
        self, page: AddOwnerPage, first_name: str, last_name: str
    ) -> None:
        page.fill_first_name(first_name)
        page.fill_last_name(last_name)
        page.fill_address(self.faker.street_address())
        page.fill_city(self.faker.city())
        page.fill_telephone_number(self.faker.msisdn()[:10])
