from UserSubscriptions.mapping import indexName as subscriptionIndex
import elasticsearch
from Utils.api import getRecord,updateRecord,insertRecord
from ContentFeatures.service import getFeaturesWithId as getMovieFeaturesWithId
from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from UserFeatures.mapping import indexName as featureIndex

#data element is a list
# [ movieId, duration ]



def updateSubscriptions(id, dataElement):
    try:
        record = getRecord(subscriptionIndex,id)

    except elasticsearch.exceptions.NotFoundError:
        insertRecord(subscriptionIndex,{
            "id":id,
            "subscriptions":[dataElement]
        })
        return

    
    data= record["_source"]
    data['subscriptions'].append(dataElement)
    updateRecord(subscriptionIndex, data["id"],data)

