from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait


class PageObject:
    def __init__(self, driver: Chrome) -> None:
        self.driver = driver
        self._wait_for_page_readiness()

    def contains_text(self, text: str) -> bool:
        """To można by też zapisać jako __contains__, wtedy działałby operator 'in'."""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: text in driver.page_source
            )
            return True
        except TimeoutError:
            return False

    def _wait_for_page_readiness(self) -> None:
        WebDriverWait(self.driver, 20).until(
            lambda driver: driver.execute_script("return document.readyState;")
            == "complete"
        )
