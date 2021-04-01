import asyncio
from traceback import print_exc
from typing import Awaitable
from typing import Callable
from typing import Optional

import sentry_sdk
from aiohttp import web
from aiohttp import web_exceptions
from marshmallow import ValidationError as MarshmallowValidationError

import exceptions
from exceptions import ServerError


@web.middleware
async def exception_middleware(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.Response]],
) -> web.Response:
    sentry_event_id: Optional[str] = None

    try:
        response: web.Response = await handler(request)
        return response
    except MarshmallowValidationError as ex:
        exc: ServerError = exceptions.ValidationError(str(ex))
    except web_exceptions.HTTPBadRequest as ex:
        exc = exceptions.InputValidationError(ex.text or '')
    except web_exceptions.HTTPUnprocessableEntity as ex:
        exc = exceptions.ValidationError(ex.text or '')
    except web_exceptions.HTTPForbidden as ex:
        exc = exceptions.Forbidden(str(ex))
    except web_exceptions.HTTPNotFound as ex:
        exc = exceptions.NotFound(ex.text or '')
    except asyncio.CancelledError as ex:
        exc = exceptions.ServerError(str(ex))
    except exceptions.ServerError as ex:
        exc = ex
    except NotImplementedError:
        exc = exceptions.MethodNotImplemented()
    # nolint
    except Exception as ex:  # pylint: disable=W0703
        print_exc()
        sentry_event_id = sentry_sdk.capture_exception(ex)

        exc = exceptions.ServerError(str(ex))

    if not sentry_event_id:
        sentry_event_id = sentry_sdk.capture_exception(exc)

    return web.json_response(
        data=exc.as_dict(),
        status=exc.status_code,
        headers={'X-Sentry-ID': sentry_event_id or ''}
    )
