from abc import ABC, abstractmethod

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo


class BotFactory(ABC):

    @abstractmethod
    async def create(self, meta: LMBotMetaInfo) -> Bot:
        pass
