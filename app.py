import falcon
from routes import Ping
from routes.document import Document

api = falcon.API()
api.add_route('/ping', Ping())
api.add_route('/search', Document())
