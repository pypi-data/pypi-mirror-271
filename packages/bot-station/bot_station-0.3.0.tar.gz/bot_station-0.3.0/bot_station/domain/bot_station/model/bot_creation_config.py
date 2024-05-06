import uuid
from dataclasses import dataclass


@dataclass
class BotCreationConfig:
    name: str
    description: str
    prompt_intro: str
    add_external_context_to_prompt: bool
    add_messages_history_to_prompt: bool
    temperature: float = 0.6
    id: str = uuid.uuid4()
