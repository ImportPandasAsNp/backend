indexName = "user_subscriptions"

subscriptionMapping = {
    "properties":{
        "id": {"type": "text"},
        "subscriptions":{"type":"object", "enabled":False}
    }
}