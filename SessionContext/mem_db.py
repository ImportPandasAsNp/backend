DIM = 576

def add(feat1,feat2,alpha):
    #compute feat1*alpha + (feat2)*(1-alpha)
    result = []
    for i in range(len(feat1)):
        result.append(feat1[i]*alpha + feat2[i]*(1-alpha))

    return result

class UserSessionVector:
    def __init__(self)->None:
        self.client = dict()

    def getVector(self,userId):
        if userId not in self.client:
            return []
        return self.client[userId]
    
    def setVector(self,userId,vector):
        self.client[userId]=vector
        return
    
    def deleteVector(self,userId):
        if userId in self.client:
            del self[userId]
    
    def addVector(self,userId,movieVector,weight=0.9):
        newVector = add(self.getVector(userId),movieVector,weight)
        self.setVector(userId,newVector)
        return
    
userSessionVectorClient = UserSessionVector()
