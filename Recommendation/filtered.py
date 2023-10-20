from ContentFeatures.service import getKNNMetadataWithFeature
from UserFeatures.service import getFeaturesWithId
from Recommendation.reranking import reranking

def filterQuery(userId, queryDict):
    userFeatures = getFeaturesWithId(userId)
    movieData = getKNNMetadataWithFeature(userFeatures,queryDict,returnFeatures=True)
    movieData = reranking(userFeatures,movieData)

    for data in movieData:
        del data['feature']

    return movieData