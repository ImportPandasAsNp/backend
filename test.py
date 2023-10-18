from Utils.api import createIndex,createMapping,createSetting,closeIndex,openIndex,deleteIndex,insertRecord,getAllRecords,deleteAllRecords
from UserFeatures.mapping import featureMapping,featureSetting,indexName as featureIndex
from UserMetadata.mapping import metadataMapping,indexName as metadataIndex, dummyUser,dummyUser1
from ContentFeatures.service import getFeaturesWithContentName
from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId


if __name__ == "__main__":
    print(getNearestUsersWithId("123456"))