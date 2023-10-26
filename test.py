from Utils.api import createIndex,createMapping,createSetting,closeIndex,openIndex,deleteIndex,insertRecord,getAllRecords,deleteAllRecords,getRecord,bulkUpload
from UserFeatures.mapping import featureMapping,featureSetting,indexName as featureIndex
from UserMetadata.mapping import metadataMapping,indexName as metadataIndex, dummyUser,dummyUser1
from ContentFeatures.service import getFeaturesWithContentName,getFeaturesWithId as feat,getKNNMetadataWithContentName
from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId,getFeaturesWithId
from UserHistory.mapping import historyMapping, indexName as historyIndex
from UserHistory.update import updateHistory, updateUserFeature
from Recommendation.ContentBased import recommendBasedOnId,recommendBasedOnName
from ContentMetadata.service import getMetadataWithIds as movie
from ContentMetadata.mapping import indexName as content,contentMapping
from Recommendation.Collaborative import recommendBasedOnId as collabId
from Recommendation.reranking import getFinalRecommendationsWithId, getFinalRecommendationsWithName
from UserHistory.service import getHistoryFromNames,getHistoryFromIds
from Recommendation.filtered import *
import pandas as pd
from UserSubscriptions.mapping import subscriptionMapping,indexName as subscriptionIndex
from UserSubscriptions.service import updateUserSubscriptions
from modelfeatures import ModelEmbeddings



if __name__ == "__main__":
    # print(getKNNMetadataWithContentName('in the dark',{
    #     "rating":"U"
    # }))
    # print(getAllRecords("moviemetadata"))
    # deleteAllRecords(historyIndex)
    # deleteAllRecords(featureIndex)
    # print(featureIndex)
    # createIndex(featureIndex)
    # closeIndex(featureIndex)
    # createSetting(featureIndex,featureSetting)
    # openIndex(featureIndex)
    # createMapping(featureIndex,featureMapping)
    # deleteAllRecords(historyIndex)
    # deleteIndex(historyIndex)
    # createIndex(historyIndex)
    # createMapping(historyIndex,historyMapping)
    # insertRecord(historyIndex,{
    #     "id":"123456",
    #     "history":[['1','2'],['2','3']]
    # })
    # print(getRecord(historyIndex,'123456'))
    # updateHistory('123456',['4','5'])
    # print(getFeaturesWithId('123456')[0])
    # print(updateUserFeature('123456', ['13644510926972048555',3]))
    # time.sleep(2)
    # print(getFeaturesWithId('123456')[0])
    # print(recommendBasedOnId('123456',{
    #     'country':'india'
    # }))
    # print(movie(['13644510926972048555']))
    # print(getAllRecords(historyIndex))
    # updateHistory('123456',['13644510926972048555','2'])
    # print(getAllRecords("user_metadata",size=3))
    # print(collabId('123456'))
    # print(feat('13644510926972048555'))
    # print(movie(['220565352928732451']))
    # print(recommendBasedOnId('234567'))
    # print(getAllRecords("user_metadata",size=10))
    # print(filterQuery('234567',{
    #     'cast':['samuel l jackson','will']
    # }))
    # print(getKNNMetadataWithContentName('the prom',{

    # }))

    # data = pd.read_csv("/Users/adityaganguly/college/Hackon/backend/feats2.csv")
    # bulkUpload(movieFeat,data)
    # print(getAllRecords(movieFeat))
    # print(getHistoryFromIds(['Pv5hTosBGZBkZraVWyk8']))
    # deleteAllRecords(historyIndex)
    # print(getAllRecords(historyIndex))
    # print(getMostFrequent('Pv5hTosBGZBkZraVWyk8','genre'))
    # print(getMetadataWithArguments({
    #     'director':'chris mckay'
    # }))
    # print(content)
    # deleteIndex(content)
    # createIndex(content)
    # createMapping(content,contentMapping)
    # print(contentMapping)
    # createIndex(content)
    # createMapping(content,contentMapping)
    # print(getAllRecords(content))
    # createIndex(subscriptionIndex)
    # deleteAllRecords(subscriptionIndex)
    # createMapping(subscriptionIndex,subscriptionMapping)
    # updateUserSubscriptions('Pv5hTosBGZBkZraVWyk8','prime')
    # print(ModelEmbeddings.getEmbeddings("Show me fun"))
    # deleteAllRecords("moviefeatures")

    # deleteIndex("moviefeatures")
    # print(getAllRecords(subscriptionIndex))
    # deleteAllRecords(subscriptionIndex)
    # print(recommendOtherPlatforms('Pv5hTosBGZBkZraVWyk8'))
    # createIndex(featureIndex)
    # closeIndex(featureIndex)
    # createSetting(featureIndex, featureSetting)
    # closeIndex(featureIndex)
    # createMapping(featureIndex,featureMapping)
    # openIndex(featureIndex)
    # data = pd.read_csv("/Users/adityaganguly/college/Hackon/backend/feats3.csv")
    # bulkUpload(featureIndex,data)
    # print(getAllRecords(featureIndex))
    # openIndex(featureIndex)
    # deleteAllRecords(historyIndex)
    deleteAllRecords(historyIndex)
    deleteAllRecords(subscriptionIndex)
    deleteAllRecords(metadataIndex)
    deleteAllRecords(featureIndex)