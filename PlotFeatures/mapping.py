plotMapping = {
    "properties": {
        "type": {"type": "keyword"},
        "title": {"type": "text"},
        "director": {"type": "text"},
        "cast": {"type": "text"},
        "country": {"type": "text"},
        "release_year": {"type": "date"},
        "age_rating": {"type": "keyword"},
        "imdb_rating":{"type": "double"},
        "genre": {"type": "text"},
        "platform": {"type": "keyword"},
        "id": {"type": "text"},
        "image_url":{"type":"text"},
        "description":{"type":"text"},
        "feature":{
            "type":"knn_vector",
            "dimension":512,
            "similarity":"cosinesimil"
        }
    }
}

plotSetting = {
    "index.knn" : "true"
}

indexName = "plotfeatures"