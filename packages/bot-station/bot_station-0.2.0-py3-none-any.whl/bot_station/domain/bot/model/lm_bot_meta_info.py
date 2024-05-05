from dataclasses import dataclass

from bot_station.domain.base.const import default_prompt_intro


@dataclass
class LMBotMetaInfo:
    id: str
    name: str
    description: str
    prompt_intro: str = default_prompt_intro
    add_external_context_to_prompt: bool = True
    add_messages_history_to_prompt: bool = False
    temperature: float = 0.6
