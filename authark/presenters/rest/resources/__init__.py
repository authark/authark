from aiohttp import web
from aiohttp_jinja2 import render_template
from .... import __version__
from .token import TokenResource
from .resource import Resource
from .user import UserResource
from .rule import RuleResource
from .policy import PolicyResource
from .ranking import RankingResource


class RootResource:

    def __init__(self, spec) -> None:
        self.spec = spec

    async def get(self, request: web.Request) -> web.Response:
        if 'api' in request.query:
            return web.json_response(self.spec.to_dict())

        context = {'url': '/?api', 'version': __version__}
        response = render_template(
            'index.html', request, context)
        response.headers['Content-Type'] = 'text/html'

        return response