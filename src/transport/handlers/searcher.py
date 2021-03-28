from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import response_schema
from marshmallow import Schema
from marshmallow import fields

from transport.handlers.store import Entity


class GetRequest(Schema):
    per_one_time = fields.Int(required=False, missing=10, description='Сколько вернуть объектов')
    

class EntityResult(Schema):
    url = fields.Url(required=True, allow_none=False)
    similarity = fields.Float(required=True, allow_none=False, description='Схожесть с запросом')


class BySpeechRequest(GetRequest):
    speech = fields.Str(required=True, allow_none=False, description='Голос в base64')
    min_similarity = fields.Float(required=False, missing=0.5, description='Минимальный коэффициент схожести')
    channels = fields.Int(required=False, allow_none=False, description='')
    rate = fields.Int(required=False, allow_none=False, missing=16000, description='')
    encoding = fields.Str(required=False, allow_none=False, missing='LINEAR16', description='')
    language_code = fields.Str(required=False, allow_none=False,missing='ru-RU', description='')


class BySpeechResponse(Schema):
    text = fields.Str(required=True, description='Что было распознано из голоса')
    entities = fields.Nested(EntityResult, many=True)


class ByTextRequest(GetRequest):
    text = fields.Str(required=True, allow_none=False)
    min_similarity = fields.Float(required=False, missing=0.5, description='Минимальный коэффициент схожести')


class ByTextResponse(Schema):
    entities = fields.Nested(EntityResult, many=True)


class ByUrlRequest(GetRequest):
    url = fields.Url(required=True, allow_none=False)


class ByUrlResponse(Schema):
    entity = fields.Nested(Entity, many=False)


class GetAllRequest(GetRequest):
    pass


class GetAllResponse(Schema):
    entities = fields.Nested(Entity, many=True)


@docs(
    tags=['search'],
    summary="Поиск по голосу",
    description='''Больше информации можно найти на 
    https://cloud.google.com/speech-to-text/docs/reference/rest/v1/RecognitionConfig'''
)
@request_schema(BySpeechRequest)
@response_schema(BySpeechResponse, 200)
async def bySpeech(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Поиск по тексту"
)
@request_schema(ByTextRequest)
@response_schema(ByTextResponse, 200)
async def byText(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Поиск по url"
)
@request_schema(ByUrlRequest)
@response_schema(ByUrlResponse, 200)
async def byUrl(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


@docs(
    tags=['search'],
    summary="Получить все файлы"
)
@request_schema(GetAllRequest)
@response_schema(GetAllResponse, 200)
async def get_all(request: web.Request) -> web.Response:
    return web.json_response({'success': True})
