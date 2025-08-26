import json
import logging
import os
import pytest
import configparser
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from requests import Session

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Добавление кастомных опций для pytest."""
    parser.addoption(
        "--ui", action="store_true", help="Запуск только UI-тестов"
    )
    parser.addoption(
        "--api", action="store_true", help="Запуск только API-тестов"
    )

def pytest_collection_modifyitems(config, items):
    """Фильтрация тестов по типам."""
    if config.getoption("--ui"):
        skip_api = pytest.mark.skip(reason="Пропуск API-тестов")
        for item in items:
            if "api" in item.keywords:
                item.add_marker(skip_api)

    if config.getoption("--api"):
        skip_ui = pytest.mark.skip(reason="Пропуск UI-тестов")
        for item in items:
            if "ui" in item.keywords:
                item.add_marker(skip_ui)

@pytest.fixture(scope="session")
def config_data():
    """Фикстура для загрузки конфигурации."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    if not os.path.exists(config_path):
        logger.error(f"Файл конфигурации {config_path} не найден")
        raise FileNotFoundError(f"Файл конфигурации {config_path} не найден")
    config.read(config_path, encoding='utf-8')
    logger.info(f"Конфигурация загружена: {dict(config['selenium'])}")
    return config

@pytest.fixture(scope="session")
def test_data():
    """Фикстура для загрузки тестовых данных."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(base_dir, 'test_data.json')
    try:
        with open(test_data_path, 'r', encoding='utf-8') as file:
            logger.info(f"Тестовые данные загружены из {test_data_path}")
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"Файл тестовых данных {test_data_path} не найден, возвращается пустой словарь")
        return {"ui_tests": [], "api_tests": []}

@pytest.fixture(scope="class")
def driver(config_data):
    """Фикстура для инициализации WebDriver (только Chrome)."""
    driver = None
    try:
        options = ChromeOptions()
        if config_data.getboolean('selenium', 'headless'):
            options.add_argument("--headless=new")
        driver = Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(config_data.getint('selenium', 'timeout'))
        logger.info("WebDriver (Chrome) успешно инициализирован")
        yield driver
    except Exception as e:
        logger.error(f"Ошибка инициализации WebDriver: {e}")
        raise
    finally:
        if driver is not None:
            logger.info("Закрытие WebDriver")
            driver.quit()

@pytest.fixture(scope="session")
def api_client(config_data):
    """Фикстура для API клиента."""
    session = Session()
    logger.info("API клиент инициализирован")
    return session

@pytest.fixture(scope="session")
def headers():
    """Фикстура для HTTP-заголовков."""
    return {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
