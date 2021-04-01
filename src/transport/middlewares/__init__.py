from aiohttp_apispec import validation_middleware

from transport.middlewares.exception import exception_middleware


MIDDLEWARES = [
    exception_middleware,
    validation_middleware
]

__all__ = [
    'MIDDLEWARES'
]