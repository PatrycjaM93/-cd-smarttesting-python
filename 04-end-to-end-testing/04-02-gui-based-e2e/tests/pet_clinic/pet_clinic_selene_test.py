import pytest
from selene import be, browser, by, config


class TestPetClinicSelene:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        config.browser_name = "chrome"
        config.base_url = "http://localhost:8080"
        config.timeour = 2
        self.browser = browser
        yield
        self.browser.quit()

    def test_displays_error_message(self) -> None:
        self.browser.open_url("/")
        self.browser.element(by.link_text("OWNERS")).click()
        self.browser.element(by.link_text("ALL")).click()

        self.browser.element(by.partial_text("Jeff")).should(be.visible)
