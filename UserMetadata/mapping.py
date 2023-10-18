metadataMapping = {
    "properties": {
        "name": {"type": "text"},
        "email": {"type": "keyword"},
        "password": {"type": "keyword"},
        "country": {"type": "text"},
        "age_filter": {"type": "keyword"},
        "genre": {"type": "text"},
        "id": {"type": "text"}        
    }
}

indexName = "user_metadata"

dummyUser = {
    "name":"Aditya",
    "email":"hikeradi@gmail.com",
    "password":"abcd",
    "country":"United States",
    "age_filter":"R",
    "genre":"comedy",
    "id":"123456"
}

dummyUser1 = {
    "name":"Amartya",
    "email":"hikeradi@gmail.com",
    "password":"abcd",
    "country":"United States",
    "age_filter":"R",
    "genre":"comedy",
    "id":"234567"
}