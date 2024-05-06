import uuid

from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from bot_station.data.base.database.base_db_dto import BaseDBDto


class BotInfoDto(BaseDBDto):
    __tablename__ = "bot_meta_info"

    id: Mapped[str] = mapped_column("id", String(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    temperature: Mapped[float] = mapped_column(Float())
    prompt_intro: Mapped[str] = mapped_column(String())
    add_external_context_to_prompt: Mapped[bool] = mapped_column(Boolean())
    add_messages_history_to_prompt: Mapped[bool] = mapped_column(Boolean())

    def __repr__(self) -> str:
        return f"Bot(id={self.id!r}, name={self.name!r}, temperature={self.temperature!r}, prompt={self.prompt_intro!r})"
