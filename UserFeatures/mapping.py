indexName = "user_featuresnew"

featureMapping = {
    "properties":{
        "id": {"type": "text"},
        "feature":{
            "type":"knn_vector",
            "dimension":512,
            "similarity":"cosinesimil"
        }
    }
}

featureSetting = {
    "index.knn" : "true"
}