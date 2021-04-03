from typing import Any, Dict, List, Union

from aiohttp import web
import elasticsearch
from elasticsearch._async.client import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from exceptions import AddEntityToBDError, NotFound

# from integrations.elasticsearch import HOST, PORT, INDEX#, CLIENT


HOST = 'localhost'
PORT = 9200
INDEX = 'store'

CLIENT: AsyncElasticsearch = None


async def service(app: web.Application):
    global CLIENT
    CLIENT = AsyncElasticsearch(hosts=HOST, port=PORT)
    mapping = {
        "properties": {
            "description": {
                "type": "text"
            },
            "description_vector": {
                "type": "dense_vector",
                "dims": 512
            }
        }
    }
    await CLIENT.indices.put_mapping(index=INDEX, body=mapping)
    yield


def _gen_data(entities: List[Dict[str, Any]], ot_type, index=INDEX):
    for entity in entities:
        yield {
            '_index': index,
            "_id": entity['url'],
            '_op_type': ot_type,
            "description": entity.get('description', ''),
            "description_vector": list(entity['description_vector']),
        }


async def add_entities(entities: List[Dict[str, Any]], index=INDEX):
    # await init_store()
    try:
        result = await async_bulk(CLIENT, _gen_data(entities, ot_type='create', index=index))
    except elasticsearch.helpers.errors.BulkIndexError as ex:
        raise AddEntityToBDError([
            {
                'url': info['create']['_id'],
                'error': info['create']['error']
            }
            for info in ex.args[1]
        ])
    return result


async def get_by_url(url, index=INDEX) -> dict:
    try:
        result = await CLIENT.get(index, id=url, _source_excludes='description_vector')
        return dict(
            url=result['_id'],
            description=result['_source']['description']
        )
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(debug=ex.args[-1])


async def get_by_description_vector(
        description_vector, page: int = 1, size: int = 10, min_similarity: float = 0.6, index=INDEX
) -> List[Dict[str, Union[int, str]]]:
    result = await CLIENT.search(index=index, body={
        "size": size,
        "from": max(0, page - 1) * size,
        "min_score": min_similarity,
        "_source": {
            "includes": ['url', 'description']
        },
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "double value = cosineSimilarity(params.description_vector, 'description_vector');"
                              "if (value < 1) {"
                              "    return 1 - Math.acos(value) / Math.PI"
                              "}"
                              "return 1",
                    "params": {
                        "description_vector": description_vector
                    }
                }
            }
        }
    })

    return {
        'all': result['hits']['total']['value'],
        'entities': [
            {
                'url': res['_id'],
                'similarity': res['_score'],
            }
            for res in result['hits']['hits']
        ]
    }


async def update(url, new_description, new_description_vector, index=INDEX):
    try:
        result = await CLIENT.update(index, id=url, body={
            'doc': {
                'description': new_description,
                'description_vector': new_description_vector,
            }
        })
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(ex.args[-1])
    return result


async def delete(url, index=INDEX):
    try:
        result = await CLIENT.delete(index, id=url)
        return result
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(ex.args[-1])


# async def get_all(page: int = 1, size: int = 10, index=INDEX):
#     result = await CLIENT.search(index='test_imgs', body={
#         "size": size,
#         "from": max(0, page - 1) * size,
#         "_source": {
#         "includes": ['url', 'description']
#     },
#         "query": {
#             "match_all": {}
#         }
#     })
#     return {'entities': [
#         {
#             'url': res['_id'],
#             'description': res['_source']['description']
#         }
#         for res in result['hits']['hits']
#     ]}
