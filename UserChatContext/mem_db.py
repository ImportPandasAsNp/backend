from Utils.helpers import mergeContext
class UserChatClient:
    def __init__(self) -> None:
        self.client = None
    
    def getClient(self):
        if self.client is None:
            self.client = dict()
        return self.client
    
    def getContext(self, userId):
        if userId not in self.client.keys():
            self.client.setdefault(userId, { 'title': 'unknown',	'director': [],	'genre': [], 'cast': [], 'plot': '' })
        return self.client[userId]
    
    def addContext(self, userId, context):
        self.client[userId] = mergeContext(self.getContext(userId), context)
        return self.client[userId]
    
    def removeContext(self, userId):
        self.client[userId] = dict()

userChatClient = UserChatClient()