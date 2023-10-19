from UserFeatures.service import getFeaturesWithId as getUserFeaturesWithId
from ContentFeatures.service import getKNNMetadataWithFeature
from UserMetadata.service import getIdsWithArguments as getUserIdsWithArguments

def recommendBasedOnId(userId, queryDict = None):
    feat = getUserFeaturesWithId(userId)
    movies = getKNNMetadataWithFeature(feat, queryDict)

    return movies

def recommendBasedOnName(userName, queryDict):
    idList = getUserIdsWithArguments({
        "name":userName
    })

    if len(idList)==0:
        return []
    
    return recommendBasedOnId(idList[0], queryDict)