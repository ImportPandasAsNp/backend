from UserSubscriptions.mapping import indexName as subscriptionIndex
from Utils.api import getRecord
from UserMetadata.service import getIdsWithArguments
from UserMetadata.mapping import indexName as userMetadataIndex
from UserSubscriptions.update import updateSubscriptions
from ContentMetadata.service import getMetadataWithIds
from es import esclient

client = esclient.getClient()

def getSubscriptionsFromId(id):
    data = getRecord(subscriptionIndex,id)

    if len(data.keys())==0:
        return []
    
    else:
        return data['_source']['subscriptions']
    
def updateUserSubscriptions(id, data):
    updateSubscriptions(id,data)