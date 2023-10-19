from UserHistory.mapping import indexName as historyIndex

from Utils.api import getRecord,updateRecord,insertRecord
from ContentFeatures.service import getFeaturesWithId as getMovieFeaturesWithId
from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from UserFeatures.mapping import indexName as featureIndex

#data element is a list
# [ movieId, duration ]

def add(feat1,feat2,alpha):
    #compute feat1*alpha + (feat2)*(1-alpha)
    result = []
    for i in range(len(feat1)):
        result.append(feat1[i]*alpha + feat2[i]*(1-alpha))

    return result


def updateHistory(id, dataElement):
    try:
        record = getRecord(historyIndex,id)

    except Exception:
        insertRecord(historyIndex,{
            "id":id,
            "history":[dataElement]
        })

    
    data= record["_source"]
    data['history'].append(dataElement)
    updateRecord(historyIndex, data)

    updateUserFeature(id,dataElement)

def updateUserFeature(id,dataElement):
    movieId = dataElement[0]

    moviefeat = getMovieFeaturesWithId(movieId)
    userFeat = getUserFeaturesWithId(id)

    if len(moviefeat)==0 or len(userFeat)==0:
        return
    
    updatedFeat = add(userFeat,moviefeat,0.9)
    
    record = {
        "id":id,
        "feature":updatedFeat
    }

    updateRecord(featureIndex, record)



