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
        "image_url":{"type":"text"},
        "description":{"type":"text"},
        "plot":{
            "type":"text",
            "analyzer":"plot_english"
        }
    }
}

contentSetting = {
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "english_stemmer": {
          "type":"stemmer",
          "language":   "english"
        },
        "english_keywords": {
          "type":"keyword_marker",
          "keywords": ["exclude-from-stemming"]
        },
      },
      "analyzer": {
        "plot_english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "english_keywords",
            "english_stemmer"
          ]
        }
      }
    }
  }
}

indexName = "moviemetadata1"
plotIndexName = "moviemetadata2"