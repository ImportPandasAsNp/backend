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

def reranking(userFeature, movieContent,returnDot=False):
    movieContent = sorted(movieContent, key=lambda x:dotProduct(userFeature,x['feature']),reverse=True)

    if returnDot:
        for x in movieContent:
            x['dot'] = dotProduct(userFeature,x['feature'])
    return movieContent

#merge content based and collab based and rerank
def getFinalRecommendationsWithId(id, queryDict=None):
    print(queryDict)
    userFeatures = getUserFeaturesWithId(id)
    
    if len(userFeatures)==0:
        movieData = getMetadataWithArguments({
            "genre":queryDict["genre"],
            "rating":queryDict["rating"],
            "subscribed_platforms":queryDict["subscribed_platforms"]
        })

        return random.sample(movieData,min(len(movieData),20))
    
    else:
        del queryDict['genre']

    if queryDict=={}:
        queryDict=None
    
    contentBased = contentId(id, queryDict,returnFeatures=True)
    collabBased = collabId(id,queryDict,returnFeatures=True)
    contentBased.extend(collabBased)

    contentBased = reranking(userFeatures,contentBased)

    if len(contentBased)==0:
        return []

    for data in contentBased:
        del data['feature']

    contentBased.pop(0)

    if len(contentBased)<20:
        return contentBased
    
    return contentBased[0:20]

def getFinalRecommendationsWithName(userName, queryDict=None):
    idList = getIdsWithArguments({
        "name":userName
    })

    if len(idList)==0:
        return []
    
    return getFinalRecommendationsWithId(idList[0], queryDict=queryDict)

