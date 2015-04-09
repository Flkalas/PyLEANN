import os

class LOGGER(object):
    def __init__(self):
        pass
    
    def initLogger(self,pathBasic="./results/"):
        self.pathBasic = pathBasic
        self.findPrefixNumber()

    def writePrefixFile(self):
        fileOpened = open(self.pathBasic + str(self.prefix) + ".chk",'w')
        fileOpened.close()
        pass
            
    def findPrefixNumber(self):
        i = 0
        while not os.path.isfile(self.pathBasic + str(i) + ".chk"):
            i += 1
        
        self.prefix = i        
        self.writePrefixFile()
        
        return self.prefix
    
    def getFileName(self):
        pass
    
    def writeTrainPercent(self,numSimulation,numGeneration,percent,numBlock=-1):
        pass
            
    def writeDiversity(self,numSimulation,numGeneration,content,numBlock=-1):
        pass

    def writeStructure(self,numSimulation,numBlock=-1):
        pass
    
    def writeTestPercent(self,numSimulation,numBlock=-1):
        pass
