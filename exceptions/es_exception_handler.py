import json
from json.decoder import JSONDecodeError
from elasticsearch.exceptions import ConnectionError, NotFoundError, RequestError
from falcon import HTTP_503, HTTP_500, HTTP_404, HTTP_400, HTTP_422

class ESExceptionHandler:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, response, *args, **kwargs):
        try:
            return self.func(self, request, response, *args, **kwargs)
        except ConnectionError as exc:
            print(exc)
            response.status = HTTP_503
            response.body = json.dumps({
                'status': 'Failure',
                'message': 'Failed to establish a new connection to ES server'
            })
        except RequestError as exc:
            print(exc)
            response.status = exc.status_code
            response.body = json.dumps({
                'status': 'Failure',
                'message': exc.error or 'We are not able to access the ES server at the moment.'
            })
        except NotFoundError as exc:
            print(exc)
            response.status = HTTP_404
            response.body = json.dumps({
                'status': 'Failure',
                'message': 'No records found matching the input criteria'
            })
        except JSONDecodeError as exc:
            print(exc)
            response.status = HTTP_400
            response.body = json.dumps({
                'status': 'Failure',
                'message': 'JSON provided in request body is not valid'
            })
        except AssertionError as exc:
            print(exc)
            message = str(exc)
            if not message:
                message = 'Please make sure the request is valid'
            response.status = HTTP_422
            response.body = json.dumps({
                'status': 'Failure',
                'message': message
            })
        except Exception as exc:
            print(exc)
            response.status = HTTP_500
            response.body = json.dumps({
                'status': 'Failure',
                'message': 'Something went wrong while processing the request'
            })
