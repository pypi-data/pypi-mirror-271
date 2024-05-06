from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage, LMBotMessage
from bot_station.domain.bot.model.lm_train_data import TrainData


class TestBot(Bot):
    next_answer = ""

    async def train(self, data: TrainData):
        pass

    async def call(self, question: LMUserMessage) -> CallResult:
        return CallResult(answer=LMBotMessage(text=self.next_answer, chat_id=question.chat_id), relevant_docs=[])

    async def load(self, meta: LMBotMetaInfo):
        pass

    async def clear(self):
        pass

    def set_next_answer(self, answer: str):
        self.next_answer = answer


class TestBotFactory(BotFactory):
    bot: Bot = TestBot()

    def set_bot(self, bot: Bot):
        self.bot = bot

    async def create(self, meta: LMBotMetaInfo) -> Bot:
        return self.bot
