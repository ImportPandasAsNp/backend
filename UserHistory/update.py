from UserHistory.mapping import indexName as historyIndex
import elasticsearch
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

def getWeightage(dataElement,watchHistory):
    minValue = 0.2
    maxValue = 0.9

    averageDuration = (sum(int(i[1]) for i in watchHistory))/len(watchHistory)

    fraction = min(averageDuration,dataElement[1])/averageDuration

    return minValue+((maxValue-minValue)*fraction)

def updateHistory(id, dataElement):
    print(dataElement)
    try:
        record = getRecord(historyIndex,id)

    except elasticsearch.exceptions.NotFoundError:
        insertRecord(historyIndex,{
            "id":id,
            "history":[dataElement]
        })
        movieFeatures = getMovieFeaturesWithId(dataElement[0])
        insertRecord(featureIndex,{
            "id":id,
            "feature":movieFeatures
        })

        return

    
    data= record["_source"]
    prevHistory = data['history']
    data['history'].append(dataElement)
    updateRecord(historyIndex, data["id"],data)

    updateUserFeature(id,dataElement,prevHistory)

def updateUserFeature(id,dataElement,prevHistory=None):
    movieId = dataElement[0]

    moviefeat = getMovieFeaturesWithId(movieId)
    userFeat = getUserFeaturesWithId(id)

    if len(moviefeat)==0 or len(userFeat)==0:
        return
    
    weight=0.9

    if prevHistory is not None:
        weight=  getWeightage(dataElement,prevHistory)
    updatedFeat = add(moviefeat,userFeat,weight)
    
    record = {
        "id":id,
        "feature":updatedFeat
    }

    updateRecord(featureIndex, record["id"], record)



