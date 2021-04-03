from aiohttp import web
from marshmallow import fields
from transport.handlers import store
from transport.handlers import searcher


def setup_routes(app: web.Application):
    app.router.add_get(r'/api/entity/get/byText{page:/?\d*}', searcher.byText, allow_head=False)
    # app.router.add_get(r'/api/entity/get/all/{page:\d?}', searcher.get_all, allow_head=False)
    app.router.add_get('/api/entity/get/byUrl', searcher.byUrl, allow_head=False)
    app.router.add_post(r'/api/entity/get/bySpeech{page:/?\d*}', searcher.bySpeech)
    
    app.router.add_put('/api/entity', store.add)
    app.router.add_post('/api/entity', store.update)
    app.router.add_delete('/api/entity', store.delete)
