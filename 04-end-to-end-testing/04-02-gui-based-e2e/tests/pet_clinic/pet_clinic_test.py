import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestPetClinic:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.faker = Faker()

        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8080")

        yield

        # Zamknięcie Driver'a (i okna przeglądarki) po teście
        self.driver.quit()

    def test_adding_owner(self) -> None:
        """Test co prawda COŚ weryfikuje, ale jest bardzo nieczytelny
        i trudny do utrzymania."""
        find_owners: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "OWNERS"))
        )
        find_owners.click()

        # Zastosowanie waitów przy przejściach na kolejne strony
        add_owner_button: WebElement = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "REGISTER"))
        )
        add_owner_button.click()

        first_name, last_name = self.faker.first_name(), self.faker.last_name()
        first_name_input: WebElement = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )
        first_name_input.send_keys(first_name)

        last_name_input = self.driver.find_element_by_name("lastName")
        last_name_input.send_keys(last_name)

        address_input = self.driver.find_element_by_name("address")
        address_input.send_keys(self.faker.street_address())

        city_input = self.driver.find_element_by_name("city")
        city_input.send_keys(self.faker.city())

        telephone_input = self.driver.find_element_by_name("telephone")
        telephone_input.send_keys(self.faker.msisdn()[:10])

        add_owner_submit = self.driver.find_element_by_xpath(
            "/html/body//owner-form//button"
        )
        add_owner_submit.click()

        WebDriverWait(self.driver, 20).until(
            lambda driver: first_name in driver.page_source
            and last_name in driver.page_source
        )

        full_name = f"{first_name} {last_name}"
        assert full_name in self.driver.page_source
