from aiohttp import web


async def handle(request: web.Request) -> web.Response:
    name = request.match_info.get('name', 'Anonymous')
    text = "Hello, " + name
    return web.Response(text=text)


app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)


if __name__ == '__main__':
    web.run_app(app)
