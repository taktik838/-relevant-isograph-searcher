from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import response_schema
from marshmallow import Schema
from marshmallow import fields

from transport.handlers import Entity

 

class AddRequest(Schema):
    entity = fields.Nested(
        nested=Entity,
        many=True,
        required=True,
        description="Файл или проект",
    )


class AddResponse(Schema):
    success = fields.Bool(required=True, allow_none=False, description='Добавилась запись в elasticsearch или нет')
    id = fields.Str(required=False, allow_none=False, description='Id записи в elasticsearch')
    error_message = fields.Str(required=False, allow_none=False, description='Почему запись не была добавлена. Только если seccess=false') 


@docs(
    tags=['search'],
    summary="Поиск по голосу"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def bySpeech(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Поиск по тексту"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def byText(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Поиск по url"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def byUrl(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Получить все файлы"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def get_all(request: web.Request) -> web.Response:
    return web.json_response({'success': True})