import logging
from typing import Any, Callable

import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from starlette import status

from bot_station.api.rest.model.bot_call_dto import BotCallDto
from bot_station.api.rest.model.bot_call_result import (
    BotCallResult,
    BotNotFoundCallResult,
    BotAnswerCallResult,
)
from bot_station.api.rest.model.bot_creation_dto import BotCreationDto
from bot_station.api.rest.model.bot_creation_result import BotCreationResult
from bot_station.api.rest.model.bot_dto import BotDto
from bot_station.api.rest.model.bot_train_dto import BotTrainDto
from bot_station.api.rest.model.bot_train_result import BotTrainResult
from bot_station.api.rest.model.web_app_config import WebAppConfig
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.model.document import Document
from bot_station.domain.bot.model.lm_bot_meta_info import LMBotMetaInfo
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.bot.model.lm_train_data import DocumentsTrainData
from bot_station.domain.bot_station.bot_station import BotStation
from bot_station.domain.bot_station.model.bot_creation_config import BotCreationConfig


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            logging.debug(
                f"--> {request.method} {request.url}\nBody: {await request.body()};\nHeaders: {request.headers}"
            )
            response: Response = await original_route_handler(request)
            logging.debug(f"<-- {response.status_code} {response.body}")
            return response

        return custom_route_handler


router = APIRouter(route_class=LoggingRoute)


@router.post("/create", status_code=200, response_model=BotCreationResult)
async def create(*, dto: BotCreationDto) -> Any:
    logging.debug(f"/create dto : {dto}")
    bot_id: str = await BotStationWebApp.create(dto)
    return BotCreationResult(id=bot_id)


@router.post("/train", status_code=200)
async def train(*, dto: BotTrainDto) -> Any:
    logging.debug(f"/train dto : {dto}")
    result: BotTrainResult = await BotStationWebApp.train(dto)
    if result is BotTrainResult.SUCCESS:
        return Response(status_code=status.HTTP_200_OK)
    if result is BotTrainResult.BOT_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/call", status_code=200, response_model=BotAnswerCallResult)
async def call(*, dto: BotCallDto) -> Any:
    logging.debug(f"/call dto : {dto}")
    result: BotCallResult = await BotStationWebApp.call(dto)
    if isinstance(result, BotNotFoundCallResult):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if isinstance(result, BotAnswerCallResult):
        logging.debug(f"/call return response : {result}")
        return result
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/admin/bots", status_code=200, response_model=list[BotDto])
async def get_all_bots() -> Any:
    logging.debug("/admin/bots")
    result = await BotStationWebApp.get_all_bots()
    logging.debug(f"/admin/bots count {len(result)}")
    return result


@router.delete("/admin/{bot_id}", status_code=200)
async def delete(*, bot_id: str) -> Any:
    logging.debug(f"/delete {bot_id}")
    is_deleted = await BotStationWebApp.delete(bot_id=bot_id)
    if is_deleted:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


def run_server():
    uvicorn.run(BotStationWebApp.api, host="0.0.0.0", port=8000)


class BotStationWebApp(object):
    api: FastAPI
    bot_station: BotStation = None

    @staticmethod
    def prepare(bot_station: BotStation, config: WebAppConfig):
        BotStationWebApp.bot_station = bot_station
        BotStationWebApp.api = FastAPI(
            title=config.title, debug=config.debug, version=config.version
        )
        BotStationWebApp.api.include_router(router)

    @staticmethod
    def launch():
        run_server()

    @staticmethod
    async def create(dto: BotCreationDto) -> str:
        config = BotCreationConfig(
            name=dto.name,
            description=dto.description,
            prompt_intro=dto.prompt_intro,
            add_external_context_to_prompt=dto.add_external_context_to_prompt,
            add_messages_history_to_prompt=dto.add_messages_history_to_prompt,
            temperature=dto.temperature,
        )
        meta_info: LMBotMetaInfo = await BotStationWebApp.bot_station.create(config)
        return meta_info.id

    @staticmethod
    async def train(dto: BotTrainDto) -> BotTrainResult:
        bot: Bot | None = await BotStationWebApp.bot_station.get_bot(bot_id=dto.bot_id)
        if bot is None:
            return BotTrainResult.BOT_NOT_FOUND
        else:
            await bot.train(
                DocumentsTrainData(
                    docs=[
                        Document(
                            data=dto.data,
                            id=dto.id,
                            source_link=dto.source_link,
                            metadata=dto.metadata,
                        )
                    ]
                )
            )
            return BotTrainResult.SUCCESS

    @staticmethod
    async def call(dto: BotCallDto) -> BotCallResult:
        bot: Bot | None = await BotStationWebApp.bot_station.get_bot(bot_id=dto.bot_id)
        if bot is None:
            return BotNotFoundCallResult()
        else:
            text = dto.data
            call_result = await bot.call(
                question=LMUserMessage(text=text, chat_id=dto.chat_id)
            )
            answer_text = call_result.answer.text
            return BotAnswerCallResult(
                text=answer_text, relevant_docs=call_result.relevant_docs
            )

    @staticmethod
    async def get_all_bots() -> list[BotDto]:
        bots_info = await BotStationWebApp.bot_station.get_bots_list()
        return [
            BotDto(
                id=b.id,
                name=b.name,
                description=b.description,
                prompt_intro=b.prompt_intro,
                add_external_context_to_prompt=b.add_external_context_to_prompt,
                add_messages_history_to_prompt=b.add_messages_history_to_prompt,
                temperature=b.temperature,
            )
            for b in bots_info
        ]

    @staticmethod
    async def delete(bot_id: str) -> bool:
        return await BotStationWebApp.bot_station.delete(bot_id=bot_id)
