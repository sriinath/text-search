from elasticsearch import Elasticsearch

class Connection:
    def __init__(self, config={}):
        self.es = Elasticsearch(**config)

    def create_document(self, index_name, document_body, document_id=''):
        return self.es.index(index_name, document_body, id=document_id)

    def get_document(self, index_name, id):
        return self.es.get(index=index_name, id=id)

    def search_document(self, index_name, search_query):
        return self.es.search(index=index_name, body=search_query)
