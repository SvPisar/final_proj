# ⚙️ Автоматизация тестирования сайта «Сервис Яндекс по доставке еды Деливери»

## Описание проекта

Этот проект содержит автотесты для сайта [Сервис Яндекс по доставке еды Деливери](https://market-delivery.yandex.ru/) — оказывающего услуги информационного взаимодействия потребителей и организаций общественного питания (рестораны, кафе и т.п.), на территории Российской Федерации.
Автотесты реализованы на Python с использованием `pytest`, `selenium`, `requests` и `allure`.  
Цель проекта — автоматизировать ключевые сценарии пользовательского взаимодействия (UI) и API, на основе тест-кейсов из финального проекта по ручному тестированию [Ссылка на финальный проект по ручному тестированию](https://testir.yonote.ru/share/f8355f9c-fe64-434d-b223-884048bf20ae).

## 🗂 Структура проекта

FINAL_PROJ/
│
├── .pytest_cache/            # Кэш pytest
├── allure-files/             # Отчеты Allure
├── tests_run/                # Директория с тестами
│   ├── __init__.py           # Позволяет Python видеть эту папку как пакет
│   ├── conftest.py           # Конфигурация pytest
│   ├── test_api.py           # Тесты для API
│   ├── test_ui.py            # Тесты для UI
│   └── test_data.json        # JSON с тестовыми данными
│
├── pages/                    # Page Object модели
│   ├── __init__.py           # Позволяет Python видеть эту папку как пакет
│   ├── base_page.py          # Базовая страница
│   ├── main_page.py          # Главная страница
│
├── requirements.txt          # Зависимости проекта
├── config.ini                # Конфигурация проекта
├── README.md                 # Описание проекта
└── .gitignore                # Игнорируемые файлы и папки для git

## 🚀 Шаги

1. Склонировать проект: [git clone](https://github.com/SvPisar/pytest_ui_api_template.git)
2. Установить зависимости  
3. Запустить тесты 'pytest'
'pytest -m ui'                 # Только UI тесты  
'pytest -m api'                # Только API тесты
'pytest -m 'название метки'    # Отдельные тесты по маркировке из файла pytest.ini
'pytest --markers'             # Список маркеров
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'
  
## 🧪 Покрытие автотестами

UI-тесты (Selenium + PageObject):

- Возможность поиска при увеличении масштаба
- Доступность политики конфиденциальности  
- Возможность выбора категории блюда в футере  
- Возможность поиска с помощью клавиатуры
- Авторизация с невалидным номером телефона

API-тесты (requests):

- Поиск блюда с валидным названием
- Поиск блюда с названием на английском языке  
- Поиск организации общественного питания  
- Поиск со значением "0"
- Поиск в несуществующей локации

## ⚙️ Стек

- pytest
- selenium
- requests
- allure
- config
- configparser
- json
- sqlalchemy

## 📌 Библиотеки

- pyp install pytest
- pip install selenium
- pip install webdriver-manager
- pip install allure-pytest

## 💬 Комментарии

- Все чувствительные данные вынесены в `config.py`  
- Проект не содержит лишних файлов: `chromedriver.exe`, `.vscode`, `__pycache__` и т.д.  
- Код оформлен по стандарту PEP8  
- Используется маркировка тестов `@pytest.mark.ui` и `@pytest.mark.api` для выборочного запуска
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)


### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager 
- pip install allure-pytest
