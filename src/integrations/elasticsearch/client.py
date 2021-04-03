from typing import Any, Dict, List, Union
import elasticsearch
from elasticsearch.helpers import async_bulk
from elasticsearch import AsyncElasticsearch
from exceptions import AddEntityToBDError, NotFound

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT


_ElasticClient = AsyncElasticsearch(hosts=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT)
_MAPING_FOR_STORE_IS_CREATED: bool = False
_INDEX = 'store'


def _gen_data(entities: List[Dict[str, Any]], ot_type, index=_INDEX):
    for entity in entities:
        yield {
            '_index': index, 
            "_id": entity['url'],
            '_op_type': ot_type,
            "description": entity.get('description', ''), 
            "description_vector": list(entity['description_vector']), 
        }
        
        
# async def init_store() -> None:
#     if _MAPING_FOR_STORE_IS_CREATED:
#         return
#     mapping = {
#         "properties": {
#             "description": {
#                 "type": "text"
#             },
#             "description_vector": {
#                 "type": "dense_vector",
#                 "dims": 512
#             }
#         }
#     }
#     await _ElasticClient.indices.put_mapping(index=_INDEX, body=mapping)
#     _MAPING_FOR_STORE_IS_CREATED = True
    

async def add_entities(entities: List[Dict[str, Any]], index=_INDEX):
    # await init_store()
    try:
        result = await async_bulk(_ElasticClient, _gen_data(entities, ot_type='create', index=index))
    except elasticsearch.helpers.errors.BulkIndexError as ex:
        raise AddEntityToBDError([
            {
                'url': info['create']['_id'],
                'error': info['create']['error']
            }
            for info in ex.args[1]
        ])


async def get_by_url(url, index=_INDEX) -> dict:
    try:
        result = await _ElasticClient.get(index, id=url, _source_excludes='description_vector')
        return dict(
            url=result['_id'],
            description=result['_source']['description']
        )
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(debug=ex.args[-1])


async def get_by_description_vector(
        description_vector, page: int = 1, size: int = 10, min_similarity: float = 0.6, index=_INDEX
    ) -> List[Dict[str, Union[int, str]]]:
    result = await _ElasticClient.search(index=index, body={
        "size": size,
        "from": max(0, page - 1) * size,
        "min_score": min_similarity,
        "_source": {
            "includes": ['url', 'description']
        },
        "query": {
            "script_score": {
                "query" : {"match_all": {}},
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
        'all': result['took'],
        'entities': [
            {
                'url': res['_id'],
                'similarity': res['_score'],
            }
            for res in result['hits']['hits']
        ]
    }
    

async def update(url, new_description, new_description_vector, index=_INDEX):
    try:
        result = await _ElasticClient.update(index, id=url, body={
            'doc': {
                'description': new_description,
                'description_vector': new_description_vector,
            }
        })
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(ex.args[-1])
    return result
    

async def delete(url, index=_INDEX):
    try:
        result = await _ElasticClient.delete(index, id=url)
        return result
    except elasticsearch.exceptions.NotFoundError as ex:
        raise NotFound(ex.args[-1])


# async def get_all(page: int = 1, size: int = 10, index=_INDEX):
#     result = await _ElasticClient.search(index='test_imgs', body={
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
