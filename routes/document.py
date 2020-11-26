import json
from falcon import HTTP_200, HTTP_201, HTTP_500

from services.es.connection import Connection
from exceptions.es_exception_handler import ESExceptionHandler
from constants import ELASTIC_CONFIG

client = Connection(config=ELASTIC_CONFIG)

class Document:
    @ESExceptionHandler
    def on_post(self, req, res):
        index_name = req.get_header('index_name')
        document = json.load(req.bounded_stream)
        created_document = client.create_document(
            index_name, document
        )
        if created_document.get('result') == 'created':
            res.status = HTTP_201
            res.body = json.dumps({
                'status': 'Success',
                'document': created_document
            })
        else:
            res.status = HTTP_500
            res.body = json.dumps({
                'status': 'Failure',
                'message': "Unknown error on creating a document in ES",
                'document': created_document
            })
    
    @ESExceptionHandler
    def on_get(self, req, res):
        index_name = req.get_header('index_name')
        skip_es_info = json.loads(req.get_param('skip_es_info', default='true'))
        body = json.loads(req.get_param('query', default='{}'))
        result = client.search_document(
            index_name=index_name,
            search_query=body
        )
        response = {"data": result.get('hits', {}).get('hits', {})} if skip_es_info else result
        res.status = HTTP_200
        res.body = json.dumps({
            "data": response
        })
