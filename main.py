import os
import random
from elasticsearch import Elasticsearch

# connection parameters

ES_CONNECTION_URL = "http://elastic:{ES_PASSWORD}@{ES_SERVER_ADDR}:9200/"

# document structure

ES_INDEX = "demo_index"
ES_DOCTYPE = "events"
ES_KEYWORD = "Handbill not printed"

# queries

ES_QUERY_TEST = {
    "query": {
        "match": {
            "message": ES_KEYWORD
        }
    }
}

ES_QUERY_ALL = {
    "query": {
        "match_all": {}
    }
}

ES_QUERY_AGG = {
    "query": {
        "bool": {
            "must": [{
                "match": {
                    "message": ES_KEYWORD
                }
            }]
        }
    },
    "aggs": {
        "counter": {
            "terms": {
                "field": "message.keyword"
            }
        }
    }
}

# generate random log entries

def random_message():
    msgs = [ES_KEYWORD, "Handbill printed", "Handbill deleted", "Handbill created", "Handbill renewed"]
    pos = random.randint(0, len(msgs)-1)
    return msgs[pos]

def start():
    # server address from env
    ES_SERVER_ADDR = os.getenv("ES_SERVER_ADDR")
    if ES_SERVER_ADDR is None:
        print("ES_SERVER_ADDR not set")
        exit(1)

    # elastic user password from env
    ES_PASSWORD = os.getenv("ES_PASSWORD")
    if ES_PASSWORD is None:
        print("ES_PASSWORD not set")
        exit(1)

    # connect to es
    try:
        es = Elasticsearch(ES_CONNECTION_URL.format(ES_PASSWORD=ES_PASSWORD, ES_SERVER_ADDR=ES_SERVER_ADDR))
        es_info = es.info()
    except Exception:
        print("Unable to connect to elasticsearch")
        exit(1)

    print("Using elasticsearch at {} (ver. {})".format(ES_SERVER_ADDR, es_info['version']['number']))

    # delete our sample index
    if es.indices.exists(ES_INDEX):
        es.indices.delete(ES_INDEX)

    # set keyword field
    mappings = {
        "mappings": {
            ES_DOCTYPE: {
                "properties": {
                    "message": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
        }
    }

    # create index
    es.indices.create(index=ES_INDEX, body=mappings)

    # counter for testing purposes
    compare_idx = 0

    # create documents
    for i in range(1, 100):
        body = {}
        msg = random_message()
        body['event'] = i
        body['message'] = msg
        res = es.index(index=ES_INDEX, doc_type=ES_DOCTYPE, body=body, id=i)
        # print("Uploaded message #{}, result: {}".format(str(i), res['result']))
        if msg == ES_KEYWORD:
            compare_idx = compare_idx + 1

    # refresh
    es.indices.refresh(index=ES_INDEX)

    # search
    result = es.search(index=ES_INDEX, doc_type=ES_DOCTYPE, body=ES_QUERY_AGG)
    buckets = result['aggregations']['counter']['buckets']
    if len(buckets) == 0:
        print("no matches")
    else:
        doc_count = 0
        for i in buckets:
            if i.get('key') == ES_KEYWORD:
                doc_count = i.get('doc_count')
                break

        if doc_count > 3:
            print("more than 3 (actually {})".format(doc_count))
        elif doc_count == 3:
            print("exactly 3")
        else:
            print("less than 3 (actually {})".format(doc_count))

        # compare findings with test
        if doc_count == compare_idx:
            print("result correct, {} == {}".format(doc_count, compare_idx))
        else:
            print("result incorrect, {} != {}".format(doc_count, compare_idx))

    # delete index
    es.indices.delete(ES_INDEX)

if __name__ == '__main__':
    start()
