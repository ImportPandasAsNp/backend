from Recommendation.collaborative import recommendBasedOnId as collabId
from Recommendation.contentbased import recommendBasedOnId as contentId
from ContentFeatures.service import getFeaturesWithId as getContentFeaturesWithId
from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from UserMetadata.service import getIdsWithArguments
import numpy as np

def dotProduct(vector1, vector2):
    return np.dot(vector1, vector2)

def getFinalRecommendationsWithId(id, queryDict=None):
    contentBased = contentId(id, queryDict)
    collabBased = collabId(id)
    userFeatures = getUserFeaturesWithId(id)

    contentBased.extend(collabBased)

    contentBased = sorted(contentBased, key = lambda x:dotProduct(userFeatures, getContentFeaturesWithId(x["_id"])),reverse=True)

    if len(contentBased)<10:
        return contentBased
    return contentBased[0:10]

def getFinalRecommendationsWithName(userName, queryDict=None):
    idList = getIdsWithArguments({
        "name":userName
    })

    if len(idList)==0:
        return []
    
    return getFinalRecommendationsWithId(idList[0], queryDict=queryDict)

