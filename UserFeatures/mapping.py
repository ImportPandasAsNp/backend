indexName = "user_featuresnewer"

featureMapping = {
    "properties":{
        "id": {"type": "text"},
        "feature":{
            "type":"knn_vector",
            "dimension":576,
            "similarity":"cosinesimil"
        }
    }
}

featureSetting = {
    "index.knn" : "true"
}