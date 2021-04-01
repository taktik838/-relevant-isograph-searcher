from typing import Iterable, List, Union

import aiohttp
import json

ENDPOINT = 'http://localhost:8501/v1/models'

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
