import pytest
import allure
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.api
class TestAPI:

    @allure.step("Тестирование позитивных сценариев поиска")
    @pytest.mark.api_positive
    @pytest.mark.parametrize("query", [
        "Цыпленок тапака",
        "кафе",
        "pizza"
    ], ids=["chicken_tapaka", "cafe", "pizza_english"])
    def test_search_positive_cases(self, api_client, config_data, query, headers):
        url = config_data['base']['api_url']
        payload = {
            "text": query,
            "location": {"latitude": 55.7558, "longitude": 37.6173}
        }
        with allure.step(f"Поиск: '{query}'"):
            response = api_client.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=config_data.getint("api", "timeout"),
            )

        with allure.step("Проверка успешного ответа"):
            assert (
                response.status_code == 200
            ), f"Ожидался статус 200, получен {response.status_code}"
            assert response.json() is not None, "Ответ должен содержать JSON"

    @allure.step("Тестирование производительности поиска")
    @pytest.mark.api_performance
    def test_search_performance(self, api_client, config_data, headers, benchmark):
        url = config_data['base']['api_url']
        payload = {
            "text": "пицца",
            "location": {"latitude": 55.7558, "longitude": 37.6173}
        }

        def make_request():
            response = api_client.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=config_data.getint('api', 'timeout')
            )
            assert response.status_code == 200, (
                f"Ожидался статус 200, получен {response.status_code}"
            )
            response_json = response.json()
            assert "blocks" in response_json, "Ответ должен содержать поле 'blocks'"
            return response

        benchmark(make_request)
        logger.info("Тест производительности успешно завершен")

    @pytest.mark.api_negative
    @allure.step("Тестирование негативных сценариев поиска")
    @pytest.mark.parametrize(
        "test_data",
        [
            {"query": "rhfrjpz,hf", "expected_status": 200},
            {"query": "0", "expected_status": 400},
            {"query": "", "expected_status": 200},
            {"query": "   ", "expected_status": 200},
        ], ids=["non_existent", "zero", "empty", "spaces"])
    def test_search_negative_cases(self, api_client, config_data, headers, test_data):
        url = config_data["base"]["api_url"]
        payload = {
            "text": test_data["query"],
            "location": {"latitude": 55.7558, "longitude": 37.6173},
        }

        with allure.step(f"Отправка запроса с query: '{test_data['query']}'"):
            response = api_client.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=config_data.getint("api", "timeout"),
            )

        with allure.step("Проверка статус кода"):
            assert response.status_code == test_data["expected_status"], (
                f"Ожидался статус {test_data['expected_status']}, "
                f"получен {response.status_code}"
            )

    @allure.step("Тестирование неправильного HTTP-метода")
    @pytest.mark.api_negative
    def test_search_wrong_method(self, api_client, config_data, headers):
        url = config_data['base']['api_url']
        with allure.step("Отправка GET запроса вместо POST"):
            response = api_client.get(url, timeout=config_data.getint("api", "timeout"))

        with allure.step("Проверка ошибки метода"):
            assert response.status_code == 405, (
                f"Ожидался статус 405 для неправильного метода, "
                f"получен {response.status_code}"
            )
