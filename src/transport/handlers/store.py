from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import response_schema
from marshmallow import Schema
from marshmallow import fields
from services.store import add_entities, update_entity
from integrations.elasticsearch import client as es_api

 
 
class Entity(Schema):
    url = fields.Url(required=True, allow_none=False)
    description = fields.Str(required=False, allow_none=False, missing='')


class AddRequest(Schema):
    entity = fields.Nested(
        nested=Entity,
        many=True,
        required=True,
        description="Файл или проект",
    )


class AddResponse(Schema):
    success = fields.Bool(required=True, allow_none=False, description='Добавилась запись в elasticsearch или нет')
    error_message = fields.Str(required=False, allow_none=False, 
                               description='Почему запись не была добавлена. Только если seccess=false')


@docs(
    tags=['elasticsearch'],
    summary="Добавить файлы"
)
@request_schema(AddRequest)
@response_schema(AddResponse, 200)
async def add(request: web.Request) -> web.Response:
    await add_entities(request['data']['entity'])
    return web.json_response({'success': True})


class UpdateRequest(Schema):
    url = fields.Url(required=True, allow_none=False)
    new_description = fields.Str(required=False, allow_none=False, missing='')


class UpdateResponse(Schema):
    success = fields.Bool(required=True, allow_none=False, description='Обновилась запись в elasticsearch или нет')
    error_message = fields.Str(required=False, allow_none=False, 
                               description='Почему запись не была обновлена. Только если seccess=false')


@docs(
    tags=['elasticsearch'],
    summary="Изменить описание. Поиск только по url"
)
@request_schema(UpdateRequest)
@response_schema(UpdateResponse, 200)
async def update(request: web.Request) -> web.Response:
    await update_entity(url=request['data']['url'], new_description=request['data']['new_description'])
    return web.json_response({'success': True})


class DeleteRequest(Schema):
    url = fields.Str(required=True, allow_none=False)


class DeleteResponse(Schema):
    success = fields.Bool(required=True, allow_none=False, description='Удалилась запись в elasticsearch или нет')
    error_message = fields.Str(required=False, allow_none=False, 
                               description='Почему запись не была удалена. Только если seccess=false')


@docs(
    tags=['elasticsearch'],
    summary="Удалить файл. Поиск только по url"
)
@request_schema(DeleteRequest)
@response_schema(DeleteResponse, 200)
async def delete(request: web.Request) -> web.Response:
    await es_api.delete(url=request['data']['url'])
    return web.json_response({'success': True})
