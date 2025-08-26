import allure
import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tests.pages.main_page import MainPage
from urllib.parse import urlparse, parse_qs
from utils import close_popup, handle_captcha

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@allure.feature("UI Tests")
@pytest.mark.ui
class TestUI:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config_data, test_data):
        """Фикстура для инициализации страницы перед каждым тестом."""
        self.page = MainPage(driver)
        self.url = config_data['base']['base_url']
        self.test_data = test_data
        self.page.open(self.url)
        close_popup(driver)
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.info(f"Открыт URL: {self.url}")
        yield

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================

    @allure.step("Проверка базового функционала поиска")
    @pytest.mark.ui_positive
    def test_search(self, driver):
        """Проверяет базовый функционал поиска."""
        try:
            self.page.search("пицца")
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка поиска",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Поиск не выполнен: {e}")
            raise

        parsed_url = urlparse(driver.current_url)
        query_params = parse_qs(parsed_url.query)
        assert query_params.get('query', [''])[0] == "пицца", (
            f"Параметр поиска не соответствует: ожидалось 'пицца', "
            f"получено '{query_params.get('query', [''])[0]}'"
        )

    @allure.step("Проверка увеличения масштаба и поиска кнопки 'Найти'")
    @pytest.mark.ui_positive
    @pytest.mark.parametrize("test_case", [
        {"description": "Zoom 250%", "zoom_percentage": 250},
        {"description": "Zoom 200%", "zoom_percentage": 200}
    ], ids=lambda t: t['description'])
    def test_zoom_increase(self, driver, test_case):
        """Тест увеличения масштаба страницы и поиска кнопки 'Найти'."""
        zoom_percentage = test_case['zoom_percentage']
        scale = zoom_percentage / 100
        driver.execute_script(
            f"document.body.style.transform = 'scale({scale})';"
        )
        driver.execute_script(
            "document.body.style.transformOrigin = '0 0';"
        )

        current_zoom = driver.execute_script(
            "return document.body.style.transform"
        )
        current_scale = (
            float(current_zoom.split("scale(")[1].split(")")[0])
            if current_zoom and "scale" in current_zoom else 1.0
        )
        current_zoom_percentage = current_scale * 100

        assert abs(current_zoom_percentage - zoom_percentage) < 0.1, (
            f"Масштаб не установлен: {current_zoom_percentage}% "
            f"вместо {zoom_percentage}%"
        )

        try:
            find_button = self.page.wait_for_clickable(self.page.FIND_BUTTON)
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                find_button
            )
            driver.execute_script("arguments[0].click();", find_button)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="После клика по кнопке 'Найти'",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка поиска кнопки",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Клик по кнопке 'Найти' не удался: {e}")
            pytest.fail(f"Кнопка 'Найти' не найдена или не кликабельна: {e}")

    @allure.step("Проверка выбора категории 'Десерты' в футере")
    @pytest.mark.ui_positive
    def test_select_dish_category(self, driver):
        """Проверяет выбор категории 'Десерты'."""
        try:
            self.page.click_dessert_category()
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.r1vfw7r0"))
            )
            title_element = driver.find_element(By.CSS_SELECTOR, "h1.r1vfw7r0")
            assert "Доставка десертов" in title_element.text, (
                f"Ожидаемый заголовок: 'Доставка десертов', "
                f"текущий: '{title_element.text}'"
            )
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка перехода в категорию",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Переход в категорию 'Десерты' не удался: {e}")
            raise

    @allure.step("Проверка поиска с помощью клавиатуры")
    @pytest.mark.ui_positive
    def test_search_using_keyboard_navigation(self, driver):
        """Проверяет поиск с помощью клавиатуры (Tab и Enter)."""
        try:
            search_input = self.page.wait_for_clickable(self.page.SEARCH_INPUT)
            search_input.send_keys(Keys.TAB)
            search_input.send_keys("пицца")
            search_input.send_keys(Keys.ENTER)
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка поиска с клавиатуры",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Поиск с клавиатуры не удался: {e}")
            raise

        parsed_url = urlparse(driver.current_url)
        query_params = parse_qs(parsed_url.query)
        assert query_params.get('query', [''])[0] == "пицца", (
            f"Поиск не выполнен: ожидалось 'пицца', "
            f"получено '{query_params.get('query', [''])[0]}'"
        )

    @allure.step("Доступность политики конфиденциальности")
    @pytest.mark.ui_positive
    def test_footer_links(self, driver, config_data):
        """Проверяет переход по ссылкам в футере."""
        original_handle = driver.current_window_handle
        try:
            main_page = MainPage(driver)
            main_page.open(config_data['base']['base_url'])
            close_popup(driver)
            handle_captcha(driver) # Добавляем обработку CAPTCHA
            
            user_agreement_link = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "a[href*='term_of_use_dc']"
                ))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                user_agreement_link
            )
            driver.execute_script("arguments[0].click();", user_agreement_link)
            WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
            
            for handle in driver.window_handles:
                if handle != original_handle:
                    driver.switch_to.window(handle)
                    break

            # Увеличиваем таймаут и используем общий селектор
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.TAG_NAME,
                    "h1"
                ))
            )
            # Проверяем URL или заголовок страницы
            assert any(term in driver.current_url or term in driver.title for term in ["term_of_use", "agreement", "соглашение"]), (
                f"Ожидался URL или заголовок с 'term_of_use' или 'соглашение', "
                f"получен URL: '{driver.current_url}', заголовок: '{driver.title}'"
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                name="После перехода на страницу соглашения",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка перехода по ссылке",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Переход по ссылке в футере не удался: {e}")
            pytest.fail(f"Не удалось перейти по ссылке в футере: {e}")

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================

    @allure.step("Проверка входа с невалидным номером телефона")
    @pytest.mark.ui_negative
    def test_login_with_invalid_phone_number(self, driver):
        """Негативный тест: вход с невалидным номером телефона."""
        try:
            self.page.click_login_button()
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "passp-field-phone"))
            )
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка клика на кнопку 'Войти'",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Клик на кнопку 'Войти' не удался: {e}")
            raise

        handle_captcha(driver)

        try:
            phone_input = self.page.wait_for_element((By.ID, "passp-field-phone"))
            phone_input.clear()
            phone_input.send_keys("1000000000")
            submit_button = self.page.wait_for_clickable((By.ID, "passp:sign-in"))
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                submit_button
            )
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка ввода номера",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Ввод номера телефона не удался: {e}")
            pytest.fail(f"Не удалось выполнить вход: {e}")

        try:
            error_message = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "[id='field:input-phone:hint'], div.Textinput-Hint.Textinput-Hint_state_error"
                ))
            )
            assert error_message and error_message.is_displayed(), (
                "Сообщение об ошибке не отображается"
            )
            expected_errors = [
                "Недопустимый формат номера",
                "Неверный формат номера",
                "Введите корректный номер"
            ]
            assert any(text in error_message.text for text in expected_errors), (
                f"Ожидаемое сообщение: {expected_errors}, "
                f"получено: '{error_message.text}'"
            )
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Ошибка проверки сообщения",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                driver.page_source.encode('utf-8'),
                name="Page Source",
                attachment_type=allure.attachment_type.HTML
            )
            logger.error(f"Проверка сообщения об ошибке не удалась: {e}")
            pytest.fail(f"Сообщение об ошибке не найдено: {e}")
