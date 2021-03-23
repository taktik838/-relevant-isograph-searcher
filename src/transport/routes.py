from aiohttp import web
from transport.handlers import store
from transport.handlers import searcher


def setup_routes(app: web.Application):
    app.router.add_get(r'/entity/get/bySpeech/{page:\d?}', searcher.bySpeech, allow_head=False)
    app.router.add_get(r'/entity/get/byText/{page:\d?}', searcher.byText, allow_head=False)
    app.router.add_get(r'/entity/get/all/{page:\d?}', searcher.get_all, allow_head=False)
    app.router.add_get('/entity/get/{id}', searcher.byId, allow_head=False)
    
    app.router.add_put('/entity', store.add)
    app.router.add_post('/entity', store.update)
    app.router.add_delete('/entity', store.delete)
