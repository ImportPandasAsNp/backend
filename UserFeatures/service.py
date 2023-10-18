from UserFeatures.search import knnQuery, getFeature, getIdsFromResult
from UserMetadata import service


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
        'user_name':userName
    })

    contentId = 1

    if len(searchList)>0:
        contentId = searchList[0]
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
        'title':id
    })

    if len(contentId) == 0:
        return []

    return getFeaturesWithId(contentId[0])