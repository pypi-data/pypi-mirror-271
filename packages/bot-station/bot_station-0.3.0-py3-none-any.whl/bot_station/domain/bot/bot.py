from abc import abstractmethod, ABC

from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.bot.model.lm_train_data import TrainData


class Bot(ABC):
    meta: LMBotMetaInfo

    @abstractmethod
    async def load(self, meta: LMBotMetaInfo):
        pass

    @abstractmethod
    async def train(self, data: TrainData):
        pass

    @abstractmethod
    async def call(self, question: LMUserMessage) -> CallResult:
        pass

    @abstractmethod
    async def clear(self):
        pass
