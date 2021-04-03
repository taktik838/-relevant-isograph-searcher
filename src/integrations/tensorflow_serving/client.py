import asyncio
from typing import Iterable, List, Optional, Union
import pickle

import aiohttp
import json
from exceptions.base import ServerError

from integrations.redis import CLIENT as redis


TTL_CACHE: int = 60 * 60
ENDPOINT = 'http://localhost:8501/v1/models'
MODELS: tuple = (
    'embed_text',
)


async def service(app: aiohttp.web.Application):
    class TensorFlowServingError(Exception):
        pass

    async def check_model(model_name: str) -> bool:
        nonlocal session
        try:
            async with session.get(f'{ENDPOINT}/{model_name}') as response:
                if response.status == 404:
                    raise TensorFlowServingError(f'{model_name} is not found')

                data: dict = await response.json()
                if data['model_version_status'][0]['state'] != 'AVAILABLE':
                    raise TensorFlowServingError(f'{model_name} is not available')

        except aiohttp.ClientConnectorError:
            raise TensorFlowServingError('Tensorflow serving is not running')

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(
            check_model(model_name)
            for model_name in MODELS
        ))

    yield


async def embed_text(text: Union[Iterable[str], str]) -> List[List[float]]:
    if isinstance(text, str):
        texts = [text]

    cached_result: List[Optional[List[float]]] = [
        pickle.loads(cache) if cache else None
        for cache in await redis.mget(texts, encoding=None)
    ]
    no_cached: List[str] = [
        texts[i]
        for i, cache in enumerate(cached_result)
        if cache is None
    ]
    if no_cached:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                '/'.join((ENDPOINT, 'embed_text:predict')),
                data=json.dumps({'instances': no_cached})
            ) as response:
                result: List[float] = await response.json()
                if response.status >= 400:
                    raise ServerError(f'tensorflow serving: {result["error"]}')

        predictions_iter: Iterable[List[float]] = iter(result['predictions'])
        all_result: List[List[float]] = [
            cache or next(predictions_iter)
            for cache in cached_result
        ]
    else:
        all_result = cached_result

    serialization_results: List[bytes] = [
        pickle.dumps(value)
        for value in all_result
    ]
    await redis.msetex(keys=texts, values=serialization_results, timeout=TTL_CACHE)
    return all_result
