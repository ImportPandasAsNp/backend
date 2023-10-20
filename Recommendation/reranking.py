from Recommendation.collaborative import recommendBasedOnId as collabId
from Recommendation.contentbased import recommendBasedOnId as contentId
from ContentFeatures.service import getFeaturesWithId as getContentFeaturesWithId
from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from UserMetadata.service import getIdsWithArguments
from numpy.linalg import norm
import numpy as np

def dotProduct(vector1, vector2):
    return np.dot(vector1, vector2)/(norm(vector1)*norm(vector2))

def reranking(userFeature, movieContent):
    movieContent = sorted(movieContent, key=lambda x:dotProduct(userFeature,x['feature']),reverse=True)
    return movieContent

#merge content based and collab based and rerank
def getFinalRecommendationsWithId(id, queryDict=None):
    contentBased = contentId(id, queryDict,returnFeatures=True)
    collabBased = collabId(id,returnFeatures=True)
    userFeatures = getUserFeaturesWithId(id)

    contentBased.extend(collabBased)

    contentBased = reranking(userFeatures,contentBased)

    for data in contentBased:
        del data['feature']

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

