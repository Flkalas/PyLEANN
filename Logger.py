
class LOGGER(object):
    def __init__(self):
        pass
    
    def initLogger(self,pathBasic="./results/"):
        self.pathBasic = pathBasic
        self.numSimulation = 0
        self.numBlock = -1
        self.numGeneration = 0
        
    def findPrefixNumber(self):
        pass
    
    def writeTrainPercent(self,numSimulation,numGeneration,percent,numBlock=-1):
        pass
            
    def writeDiversity(self,numBlock=-1):
        pass
    
    def writeTestPercent(self,numSimulation,numBlock=-1):
        pass

    def writeStructure(self,numSimulation,numBlock=-1):
        pass