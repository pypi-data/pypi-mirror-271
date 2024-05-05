from dataclasses import dataclass


@dataclass
class YandexCloudConfig:
    api_key: str
    folder_id: str
    model_name: str
    # TODO: уйдет в другой конфиг
    qdrant_url: str | None
    qdrant_db_path: str | None
