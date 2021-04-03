import hashlib

import asyncio
from aiohttp import web
from google.cloud import speech

from integrations.redis import CLIENT as redis


AUTH_PATH: str = 'src/integrations/google/secret.json'
TTL_CACHE: int = 60 * 60

CLIENT: speech.SpeechAsyncClient


async def service(app: web.Application):
    global CLIENT
    CLIENT = speech.SpeechAsyncClient.from_service_account_file(AUTH_PATH)
    yield


async def speech2text(
        content: bytes, language_code: str = 'ru-RU', channels: int = 1, rate: int = 16000, encoding: str = 'LINEAR16'
) -> str:
    global CLIENT
    hash_file: str = hashlib.sha512(content).hexdigest()
    cache_key: str = f'speech2text_{hash_file}_{language_code}_{channels}_{rate}_{encoding}'

    cached_response: str = await redis.get(key=cache_key)
    if cached_response:
        return cached_response

    audio = speech.RecognitionAudio(content=content)
    try:
        encoding = speech.RecognitionConfig.AudioEncoding[encoding.upper()]
    except KeyError:
        raise

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=rate,
        language_code=language_code,
        audio_channel_count=channels,
    )

    response = await CLIENT.recognize(config=config, audio=audio)

    await redis.setex(
        key=cache_key, timeout=TTL_CACHE, value=response.results[0].alternatives[0].transcript
    )

    return response.results[0].alternatives[0].transcript


if __name__ == '__main__':
    async def main():
        path = 'src/integrations/google/ru16.flac'
        content = open(path, 'rb').read()
        print(await speech2text(content, encoding='flac', language_code='ru'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
