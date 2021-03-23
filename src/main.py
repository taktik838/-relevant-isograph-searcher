from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

import settings
import sentry_sdk
from transport.routes import setup_routes
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
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
    app = web.Application()
    # await self_check()
    setup_routes(app)
    setup_aiohttp_apispec(app, **settings.APISPEC_CONF)
    return app



if __name__ == '__main__':
    import uvloop

    uvloop.install()
    web.run_app(init(), port=8085)
