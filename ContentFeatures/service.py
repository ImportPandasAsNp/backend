from ContentFeatures.search import knnQuery, getFeature, getIdsFromResult
from ContentMetadata import service


def getKNNMetadataWithFeature(feat,queryDict=None,returnFeatures = False):
    knnDict = {
        'feature':feat
    }

    if queryDict is not None:
        filterIds = service.getIdsWithArguments(queryDict)
        knnDict['ids'] = filterIds
    
    res = knnQuery(knnDict)
    ids = getIdsFromResult(res)

    if len(res)>0:
        metadata = service.getMetadataWithIds(ids)

        if returnFeatures:
            id2feat = dict(zip([data["_id"] for data in res['hits']['hits']],
                    [data['_source']['feature'] for data in res['hits']['hits']]))
            
            for data in metadata:
                data['feature'] = id2feat[data["_id"]]

        return metadata

    else:
        return []


def getKNNMetadataWithContentName(contentName, queryDict=None, returnFeatures = False):
    searchList = service.getIdsWithArguments({
        'title':contentName
    })

    contentId = 1

    if len(searchList)>0:
        contentId = searchList[0]
    else:
        return []
    
    feat = getFeature(contentId)

    if len(feat)==0:
        return []

    return getKNNMetadataWithFeature(feat,queryDict, returnFeatures)

def getFeaturesWithId(id):
    return getFeature(id)

def getFeaturesWithContentName(id):
    contentId = service.getIdsWithArguments({
        'title':id
    })

    if len(contentId) == 0:
        return []

    return getFeaturesWithId(contentId[0])