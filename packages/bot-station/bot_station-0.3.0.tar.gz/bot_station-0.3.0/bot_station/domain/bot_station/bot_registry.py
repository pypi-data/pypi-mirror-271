from abc import ABC, abstractmethod
from typing import List

from bot_station.domain.bot_station.model.bot_creation_config import BotCreationConfig
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo


class BotRegistry(ABC):

    @abstractmethod
    async def create(self, config: BotCreationConfig) -> LMBotMetaInfo:
        pass

    @abstractmethod
    async def update(self, meta: LMBotMetaInfo):
        pass

    @abstractmethod
    async def get(self, bot_id: str) -> LMBotMetaInfo | None:
        pass

    @abstractmethod
    async def get_all(self) -> List[LMBotMetaInfo]:
        pass

    @abstractmethod
    async def delete(self, bot_id: str):
        pass
