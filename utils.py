import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def close_popup(driver):
    """Утилитарная функция для закрытия всплывающего окна, если оно появляется"""
    try:
        popup_locator = (By.CSS_SELECTOR, "div.r1nk4da0")
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(popup_locator)
        )
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//span[text()='Да']]"
            ))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            yes_button
        )
        yes_button.click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element(popup)
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="После закрытия окна",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("Всплывающее окно успешно закрыто")
        return True
    except Exception as e:
        logger.warning(f"Всплывающее окно не найдено или не удалось закрыть: {e}")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Ошибка закрытия попапа",
            attachment_type=allure.attachment_type.PNG
        )
        return False


def handle_captcha(driver):
    """Утилитарная функция для обработки CAPTCHA, если она появляется"""
    try:
        captcha_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(), 'Я не робот') or contains(text(), 'I\\'m not a robot')]"
            ))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            captcha_button
        )
        captcha_button.click()
        logger.info("Кнопка CAPTCHA нажата")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "passp-field-phone"))
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="После обработки CAPTCHA",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"CAPTCHA не найдена или не удалось обработать: {e}")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Ошибка обработки CAPTCHA",
            attachment_type=allure.attachment_type.PNG
        )
        driver.refresh()
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.info("Страница обновлена из-за CAPTCHA")
