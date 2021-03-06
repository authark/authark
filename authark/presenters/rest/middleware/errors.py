import logging
from traceback import format_tb
from typing import Callable
from aiohttp import web
from json import dumps
from injectark import Injectark
from ....core import Config


def errors_middleware_factory(
        config: Config, injector: Injectark) -> Callable:

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        try:
            return await handler(request)
        except Exception as error:
            type_ = type(error).__name__
            status = getattr(error, 'status', 500)
            message = str(error)
            traceback = format_tb(error.__traceback__)

            logging.exception('Service Error')

            return web.json_response({"error": {
                "type": type_,
                "message": message,
                "trace": traceback
            }}, status=status, dumps=dumps)

    return middleware
