from Recommendation.Collaborative import recommendBasedOnId as collabId
from Recommendation.ContentBased import recommendBasedOnId as contentId
from ContentFeatures.service import getFeaturesWithId as getContentFeaturesWithId
from ContentMetadata.service import getMetadataWithArguments
from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from UserMetadata.service import getIdsWithArguments
from numpy.linalg import norm
import numpy as np
import random

def dotProduct(vector1, vector2):
    return np.dot(vector1, vector2)/(norm(vector1)*norm(vector2))

def reranking(userFeature, movieContent):
    movieContent = sorted(movieContent, key=lambda x:dotProduct(userFeature,x['feature']),reverse=True)
    return movieContent

#merge content based and collab based and rerank
def getFinalRecommendationsWithId(id, queryDict=None):
    userFeatures = getUserFeaturesWithId(id)

    
    if len(userFeatures)==0 and "genre" in queryDict:
        movieData = getMetadataWithArguments({
            "genre":queryDict["genre"]
        })

        return random.sample(movieData,k=20)
    
    else:
        del queryDict['genre']

    if queryDict=={}:
        queryDict=None
        
    contentBased = contentId(id, queryDict,returnFeatures=True)
    collabBased = collabId(id,returnFeatures=True)
    contentBased.extend(collabBased)

    contentBased = reranking(userFeatures,contentBased)

    if len(contentBased)==0:
        return []

    for data in contentBased:
        del data['feature']

    contentBased.pop(0)

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

