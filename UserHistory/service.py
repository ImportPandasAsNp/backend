from UserHistory.mapping import indexName as historyIndex
from Utils.api import getRecord
from UserMetadata.service import getIdsWithArguments
from UserMetadata.mapping import indexName as userMetadataIndex
from UserHistory.update import updateHistory, updateUserFeature
from ContentMetadata.service import getMetadataWithIds
from es import esclient

client = esclient.getClient()

def getHistoryFromId(id):

    try:
        data = getRecord(historyIndex,id)

        if len(data.keys())==0:
            return []
        
        else:
            return data['_source']['history']
    except:
        return []
    
def getHistoryFromUserName(userName):
    ids = getIdsWithArguments({
        "name":userName
    })
    

    if len(ids)==0:
        return []

    return getHistoryFromId(ids[0])

def getContentMetadataHistoryFromId(id):
    history = getHistoryFromId(id)

    contentIds = [his[0] for his in history]

    idDict = dict()

    for i in range(len(contentIds)):
        idDict[contentIds[i]] = i

    metadata = getMetadataWithIds(contentIds)
    metadata.sort(key=lambda x:idDict[x["_id"]])
    return metadata

def getHistoryFromIds(idList):
    query = {
        'query':{
            'ids':{
                'values':idList
            }
        }
    }

    return client.search(index=historyIndex,body=query,size=len(idList))

def getHistoryFromNames(nameList):
    nameList = [x.lower() for x in nameList]
    query = {
        'query':{
            'terms':{
                'name':nameList
            }
        }
    }

    ids = client.search(index = userMetadataIndex,body=query,size=len(nameList))
    ids = [data["_id"] for data in ids['hits']['hits']]
    return getHistoryFromIds(ids)

def updateUserHistory(id, data):
    updateHistory(id, data)
    updateUserFeature(id, data)

