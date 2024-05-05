import logging
from abc import abstractmethod, ABC
from typing import List

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo
from bot_station.domain.bot_station.bot_registry import BotRegistry
from bot_station.domain.bot_station.model.bot_creation_config import BotCreationConfig


class BotStation(ABC):

    @abstractmethod
    async def create(self, config: BotCreationConfig) -> LMBotMetaInfo:
        pass

    @abstractmethod
    async def get_bot(self, bot_id: str) -> Bot | None:
        pass

    @abstractmethod
    async def get_bots_list(self) -> List[LMBotMetaInfo]:
        pass

    @abstractmethod
    async def delete(self, bot_id: str) -> bool:
        pass


class BotStationImpl(BotStation):
    bot_registry: BotRegistry
    bot_factory: BotFactory

    __in_memory_bots: dict[str, Bot] = {}

    def __init__(
            self,
            bot_registry: BotRegistry,
            bot_factory: BotFactory,
    ):
        self.bot_registry = bot_registry
        self.bot_factory = bot_factory

    async def create(self, config: BotCreationConfig) -> LMBotMetaInfo:
        logging.debug(f"create {config}")
        meta_info = await self.bot_registry.create(config)
        return meta_info

    async def get_bot(self, bot_id: str) -> Bot | None:
        logging.debug(f"get bot_id)")
        if bot_id is None:
            raise Exception("Bot id is None!")
        bot = self.__in_memory_bots.get(bot_id, None)
        if bot is not None:
            return bot

        meta = await self.bot_registry.get(bot_id)
        if meta is None:
            logging.warning(f"No bot_station in registry {bot_id}")
            return None
        else:
            bot = await self.bot_factory.create(meta=meta)
            self.__in_memory_bots[bot_id] = bot
            return bot

    async def get_bots_list(self) -> List[LMBotMetaInfo]:
        logging.debug("get_bots_list")
        return await self.bot_registry.get_all()

    async def delete(self, bot_id: str) -> bool:
        logging.debug(f"delete {bot_id}")
        bot = await self.get_bot(bot_id=bot_id)
        if bot is not None:
            await bot.clear()
            await self.bot_registry.delete(bot_id=bot_id)
            self.__in_memory_bots.pop(bot_id, None)
            return True
        else:
            logging.warning(f"No bot_station in registry {bot_id}")
            return False
