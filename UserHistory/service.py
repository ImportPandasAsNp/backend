from UserHistory.mapping import indexName as historyIndex
from Utils.api import getRecord
from UserMetadata.service import getIdsWithArguments
from es import esclient

client = esclient.getClient()

def getHistoryFromId(id):
    data = getRecord(historyIndex,id)

    if len(data.keys())==0:
        return []
    
    else:
        return data['_source']['history']
    
def getHistoryFromUserName(userName):
    ids = getIdsWithArguments({
        "name":userName
    })
    

    if len(ids)==0:
        return []

    return getHistoryFromId(ids[0])


def getHistoryFromIds(idList):
    query = {
        'query':{
            'ids':{
                'values':idList
            }
        }
    }

    return client.search(index=historyIndex,body=query,size=len(idList))

def getHistoryFromUserNames(nameList):
    ids = getIdsWithArguments({
        'name':nameList
    })

    return getHistoryFromIds(ids)


