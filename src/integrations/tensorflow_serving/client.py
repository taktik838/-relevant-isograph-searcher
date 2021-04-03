import asyncio
from typing import Iterable, List, Union

import aiohttp
import json

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
    

async def embed_text(text: Union[Iterable[str], str]) -> List[float]:
    if isinstance(text, str):
        text = [text]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            '/'.join((ENDPOINT, 'embed_text:predict')),
            data=json.dumps({'instances': text})
        ) as response:
            result: List[float] = await response.json()
            return result['predictions']
