indexName = "user_history"

historyMapping = {
    "properties":{
        "id": {"type": "text"},
        "history":{"type":"object", "enabled":False}
    }
}