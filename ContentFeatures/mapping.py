indexName = "moviefeatures"

featureMapping = {
    "properties":{
        "id": {"type": "text"},
        "feature":{
            "type":"knn_vector",
            "dimension":384,
            "similarity":"cosinesimil"
        }
    }
}

featureSetting = {
    "index.knn" : "true"
}