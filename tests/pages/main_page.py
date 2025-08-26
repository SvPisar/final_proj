import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.SEARCH_INPUT = (
            By.CSS_SELECTOR,
            "input[placeholder*='Найти'], input[name='search']"
        )
        self.FIND_BUTTON = (
            By.CSS_SELECTOR,
            "button.r1jyb6b1.v102ekr4, button[data-testid='search-button']"
        )
        self.DESSERT_CATEGORY = (
            By.CSS_SELECTOR,
            "a[href*='deserti']"
        )
        self.LOGIN_BUTTON = (
            By.CSS_SELECTOR,
            "button[data-testid='ui-button'], a[href*='passport'], button[class*='login']"
        )

    def open(self, url: str) -> None:
        """Открывает указанный URL."""
        self.driver.get(url)
        logger.info(f"Открыт URL: {url}")

    def search(self, query: str) -> None:
        """Выполняет поиск по заданному запросу."""
        try:
            search_input = self.wait_for_element(self.SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(query)
            find_button = self.wait_for_clickable(self.FIND_BUTTON)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                find_button
            )
            self.driver.execute_script("arguments[0].click();", find_button)
            logger.info(f"Выполнен поиск по запросу: {query}")
        except Exception as e:
            logger.error(f"Поиск по запросу '{query}' не удался: {e}")
            raise

    def click_dessert_category(self) -> None:
        """Переходит в категорию 'Десерты'."""
        try:
            dessert_button = self.wait_for_clickable(self.DESSERT_CATEGORY)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                dessert_button
            )
            self.driver.execute_script("arguments[0].click();", dessert_button)
            logger.info("Переход в категорию 'Десерты' выполнен")
        except Exception as e:
            logger.error(f"Переход в категорию 'Десерты' не удался: {e}")
            raise

    def click_login_button(self) -> None:
        """Нажимает на кнопку 'Войти'."""
        try:
            login_button = self.wait_for_clickable(self.LOGIN_BUTTON)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                login_button
            )
            self.driver.execute_script("arguments[0].click();", login_button)
            logger.info("Клик по кнопке 'Войти' выполнен")
        except Exception as e:
            logger.error(f"Клик по кнопке 'Войти' не удался: {e}")
            raise

    def wait_for_clickable(self, locator: tuple[str, str]) -> WebElement:
        """Ожидает, пока элемент станет кликабельным."""
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Элемент с локатором {locator} кликабелен")
            return element
        except Exception as e:
            logger.error(f"Не удалось найти кликабельный элемент с локатором {locator}: {e}")
            raise

    def wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        """Ожидает, пока элемент станет видимым."""
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Элемент с локатором {locator} присутствует")
            return element
        except Exception as e:
            logger.error(f"Не удалось найти элемент с локатором {locator}: {e}")
            raise
