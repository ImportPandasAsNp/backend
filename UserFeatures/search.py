import sys
import os
import re

from es import esclient
from UserFeatures.mapping import indexName
from SessionContext.mem_db import userSessionVectorClient

esclient.getClient()
client = esclient.client
aws4auth = esclient.aws_auth_client

def knnQuery(args):
    query = {
    }

    if 'ids' in args:
        query= {
            'size':10,
            'query':{
                'script_score':{
                    'query':{
                        "bool":{
                            "filter":{
                                'ids':{
                                    'values':args['ids']
                                }
                            }
                        }
                    },
                    'script':{
                        "lang": "knn",
                        'source':'knn_score',
                        'params':{
                            'field':'feature',
                            'query_value':args['feature'],
                            'space_type':'cosinesimil'
                        }
                    }
                }
            }
        }

    else:
        query = {
            "query":{
                "knn":{
                    'feature':{
                        'vector':args['feature'],
                        'k':10
                    }
                }
            }
        }


    res = client.search(index=indexName, body = query)
    return res


def getFeature(id):
    if len(userSessionVectorClient.getVector(id))!=0:
        return userSessionVectorClient.getVector(id)
    
    query = {
        'query':{
            'ids': {
                'values':[id]
            }
        }
    }

    res = client.search(index = indexName,body=query)

    if res['hits']['total']['value'] > 0:
        userSessionVectorClient.setVector(id,res['hits']['hits'][0]['_source']['feature'])
        return res['hits']['hits'][0]['_source']['feature']
    
    userSessionVectorClient.setVector(id,[])
    return []


def getIdsFromResult(res):
    return [data['_id'] for data in res['hits']['hits']]


