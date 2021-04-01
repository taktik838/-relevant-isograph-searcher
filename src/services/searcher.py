from typing import Dict, List, Union

from integrations.google.client import speech2text
from integrations.tensorflow_serving.client import embed_text
from integrations.elasticsearch.client import get_by_description_vector


async def get_by_text(text: str, page=0, size=10, min_similarity=0.6) -> Dict[str, Union[str, float]]:
    vector: List[float] = (await embed_text(text))[0]
    result = await get_by_description_vector(vector, page=page, size=size, min_similarity=min_similarity)
    return result


async def get_by_speech(
        speech: bytes, language_code: str = 'ru-RU', channels: int = 1, rate: int = 16000, encoding: str = 'LINEAR16', 
        page=0, size=10, min_similarity=0.6
    ) -> Dict[str, Union[str, float]]:
    text: str = await speech2text(speech, language_code, channels, rate, encoding)
    result = await get_by_text(text, page=page, size=size, min_similarity=min_similarity)
    return result
