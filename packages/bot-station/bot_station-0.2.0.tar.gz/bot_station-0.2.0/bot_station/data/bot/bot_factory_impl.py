import logging

from bot_station.data.bot.bot_impl import BotImpl
from bot_station.data.bot.chat_message_storage_impl import ChatMessageStorageImpl
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.domain.base.const import message_history_path
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo


class BotFactoryImpl(BotFactory):
    config: YandexCloudConfig

    def __init__(
            self,
            config: YandexCloudConfig,
    ):
        self.config = config

    async def create(self, meta: LMBotMetaInfo) -> Bot:
        logging.debug(f"create new bot {meta}")
        bot = BotImpl(
            message_storage=ChatMessageStorageImpl(
                root_message_history_path=message_history_path
            ),
            config=self.config,
        )
        await bot.load(meta=meta)
        return bot
