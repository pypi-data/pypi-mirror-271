from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class BotCreationDto(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=0, max_length=500)
    prompt_intro: str = Field(min_length=0, max_length=5000)
    add_external_context_to_prompt: bool = Field(True)
    add_messages_history_to_prompt: bool = Field(False)
    temperature: float = Field(0.6)
