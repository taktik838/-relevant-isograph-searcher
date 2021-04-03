from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from integrations import redis
from integrations.google import client as google
from integrations.elasticsearch import client as elasticsearch
from integrations.tensorflow_serving import client as tensorflow

import settings
import sentry_sdk
from transport.routes import setup_routes
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from transport.middlewares import MIDDLEWARES
# from utils.self_check import self_check


sentry_sdk.init(
    settings.SENTRY_DSN,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    integrations=[AioHttpIntegration()]
)


async def init():
    app = web.Application(middlewares=MIDDLEWARES, client_max_size=0)
    # await self_check()
    setup_routes(app)
    setup_aiohttp_apispec(app, **settings.APISPEC_CONF)
    app.cleanup_ctx.extend([
        redis.service,
        google.service,
        elasticsearch.service,
        tensorflow.service,
    ])
    return app


if __name__ == '__main__':
    import uvloop

    uvloop.install()
    web.run_app(init(), port=8085)
