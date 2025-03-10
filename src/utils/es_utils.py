"""Elasticsearch API client utilities."""
import json
import requests

from src.utils.config import config

# Initialize configuration data
_PREFIX = config()['elasticsearch_index_prefix']
_ES_URL = "http://" + config()['elasticsearch_host'] + ":" + str(config()['elasticsearch_port'])


def does_doc_exist(wsid, objid):
    """Check if a document exists on elasticsearch based on workspace and object id."""
    _id = f"WS::{wsid}:{objid}"
    resp = requests.post(
        _ES_URL + f"/{_PREFIX}.*/_search",
        data=json.dumps({'query': {'term': {'_id': _id}}}),
        params={'size': 0},
        headers={'Content-Type': 'application/json'}
    )
    if not resp.ok:
        raise RuntimeError(f"Unexpected elasticsearch server error:\n{resp.text}")
    total = resp.json()['hits']['total']
    return total > 0
