from dataclasses import dataclass


@dataclass
class Document:
    id: str
    data: str
    source_link: str | None
    metadata: dict | None
