import logging
import unittest

from fastapi.testclient import TestClient

from bot_station.api.rest.api import BotStationWebApp
from bot_station.api.rest.model.web_app_config import WebAppConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.di.bot_station_module import BotStationModule
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot_station.bot_station import BotStation
from test_bot_factory import TestBotFactory, TestBot


def launch_test_web_app(bot: Bot):
    env_config = YandexCloudConfig(
        api_key="",
        folder_id="",
        model_name="",
        qdrant_url="",
        qdrant_db_path=None,
    )
    bot_factory = TestBotFactory()
    bot_factory.set_bot(bot)
    BotStationModule.provide_bot_factory(bot_factory)
    test_bot_station: BotStation = BotStationModule.create_bot_station(env_config)

    BotStationWebApp.prepare(bot_station=test_bot_station, config=WebAppConfig())


class BotStationApiTest(unittest.TestCase):
    mock_bot = TestBot()
    bot_station_test_client: TestClient

    def setUp(self):
        launch_test_web_app(self.mock_bot)
        self.bot_station_test_client = TestClient(BotStationWebApp.api)

    def test_create(self) -> str:
        response = self.bot_station_test_client.post(
            url="/create",
            json={
                "name": "name",
                "description": "description",
                "prompt_intro": "You are programmer's assistant",
                "add_external_context_to_prompt": "true",
                "add_messages_history_to_prompt": "true",
                "temperature": 0.6
            }
        )
        logging.debug(f"response = {response.content}")
        self.assertEqual(200, response.status_code)
        return response.json()["id"]

    def test_train(self):
        bot_id: str = self.test_create()
        response = self.bot_station_test_client.post(
            url="/train",
            json={
                "bot_id": bot_id,
                "id": "1",
                "data": "FastAPI is a modern, fast, web framework for building APIs with Python.",
                "source_link": "https://aaa.ru"
            }
        )
        self.assertEqual(200, response.status_code)

    def test_train_incorrect_id(self):
        response = self.bot_station_test_client.post(
            url="/train",
            json={
                "bot_id": "-",
                "id": "1",
                "data": "FastAPI is a modern, fast, web framework for building APIs with Python.",
                "source_link": "https://aaa.ru"
            }
        )
        self.assertEqual(404, response.status_code)

    def test_call(self):
        answer = "FastAPI is a modern, web framework"

        bot_id: str = self.test_create()
        self.test_train()
        self.mock_bot.set_next_answer(answer)
        response = self.bot_station_test_client.post(
            url="/call",
            json={
                "bot_id": bot_id,
                "chat_id": 1,
                "data": "What is FastAPI?"
            }
        )
        logging.debug(f"response = {response.content}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(answer, response.json()["text"])


if __name__ == '__main__':
    unittest.main()
