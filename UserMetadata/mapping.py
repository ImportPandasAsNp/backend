contentMapping = {
    "properties": {
        "user_name": {"type": "keyword"},
        "name": {"type": "text"},
        "email": {"type": "keyword"},
        "password": {"type": "keyword"},
        "director": {"type": "text"},
        "cast": {"type": "text"},
        "country": {"type": "text"},
        "age_filter": {"type": "keyword"},
        "genre": {"type": "text"},
        "id": {"type": "text"}        
    }
}

indexName = "user_metadata"