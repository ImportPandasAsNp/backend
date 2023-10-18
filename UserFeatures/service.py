from UserFeatures.search import knnQuery, getFeature, getIdsFromResult
from UserMetadata import service
from UserMetadata.service import getMetadataWithIds


def getKNNMetadataWithFeature(feat,queryDict=None):
    knnDict = {
        'feature':feat
    }

    if queryDict is not None:
        print("Here")
        filterIds = service.getIdsWithArguments(queryDict)
        knnDict['ids'] = filterIds
    
    res = knnQuery(knnDict)
    ids = getIdsFromResult(res)
    # id2FeatDict = 
    if len(res)>0:
        metadata = service.getMetadataWithIds(ids)
        return metadata

    else:
        return []


def getKNNMetadataWithUserName(userName, queryDict=None):
    searchList = service.getIdsWithArguments({
        'name':userName
    })

    contentId = 1

    if len(searchList)>0:
        contentId = searchList[0]
        print(contentId)
    else:
        return []
    
    feat = getFeature(contentId)

    if len(feat)==0:
        return []

    return getKNNMetadataWithFeature(feat,queryDict)

def getFeaturesWithId(id):
    return getFeature(id)

def getFeaturesWithUserName(id):
    contentId = service.getIdsWithArguments({
        'name':id
    })

    if len(contentId) == 0:
        return []

    return getFeaturesWithId(contentId[0])


def getNearestUsersWithUserName(userName:str):

    nearestUsers = getKNNMetadataWithUserName(userName)

    return nearestUsers

def getNearestUsersWithId(userId:str):
    idList = getMetadataWithIds([userId])

    if len(idList)==0:
        return []

    return getKNNMetadataWithUserName(idList[0]["_source"]["name"])