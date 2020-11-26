import os
import json

ELASTIC_CONFIG = json.loads(os.environ.get('ELASTIC_CONFIG', '{}'))
