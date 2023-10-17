contentMapping = {
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
        "image_url":{"type":"text"}
    }
}

indexName = "content_metadata"