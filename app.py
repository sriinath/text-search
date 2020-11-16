import falcon

from routes import Ping

api = falcon.API()
api.add_route('/ping', Ping())
