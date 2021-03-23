from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import response_schema
from marshmallow import Schema
from marshmallow import fields


class Entity(Schema):
    id = fields.Str(required=False, allow_none=True, default=None)
    url = fields.Str(required=True, allow_none=False)
    description = fields.Str(required=False, allow_none=False, default='')
 

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
    tags=['elasticsearch'],
    summary="Запрос оформления дебетовой карты"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def add(request: web.Request) -> web.Response:
    return web.json_response()


@docs(
    tags=['elasticsearch']
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def update(request: web.Request) -> web.Response:
    return web.json_response()


@docs(
    tags=['elasticsearch']
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def delete(request: web.Request) -> web.Response:
    return web.json_response()
