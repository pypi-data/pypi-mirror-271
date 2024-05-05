from abc import ABC
from dataclasses import dataclass
from typing import List

from bot_station.domain.bot.model.document import Document


class TrainData(ABC):
    pass


@dataclass
class DocumentsTrainData(TrainData):
    docs: List[Document]

    def __repr__(self):
        return str(self.docs)


@dataclass
class QnATrainData(TrainData):
    question: str
    answer: str
