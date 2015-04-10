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
    
    def getFileName(self,numSimulation,nameCategory,numBlock=-1):        
        
        strName = "_" +self.prefix + "_" + str(numSimulation)  + "_"
        
        if numBlock != -1:
            strName += str(numBlock) + "_" 
            
        strName += nameCategory + ".csv"
        
        return strName
    
    def writeGenerationResult(self,numSimulation,numGeneration,nameCategory,strContent,numBlock=-1):
        strFileName = self.getFileName(numSimulation,nameCategory,numBlock) 
        
        if numGeneration != 0:
            modeFile = 'a'
        else:
            modeFile = 'w'
        
        fileOpend = open(strFileName,modeFile)
        
        strWrite = str(numGeneration)+","+strContent        
        fileOpend.write(strWrite)
        
        return fileOpend.close()
    
    def writeBlockResult(self,numSimulation,nameCategory,strContent,numBlock=-1):
        strFileName = self.getFileName(numSimulation,nameCategory,numBlock) 
        
        fileOpend = open(strFileName,'w')
        fileOpend.write(strContent)
        
        return fileOpend.close()
    
    def writeSimulationResult(self,numSimulation,nameCategory,strContent,numBlock=-1):
        strFileName = self.getFileName(numSimulation,nameCategory) 
        
        if numBlock > 0:
            modeFile = 'a'
        else:
            modeFile = 'w'
        
        strWrite = str(numBlock) + "," + strContent
        
        fileOpend = open(strFileName,modeFile)
        fileOpend.write(strWrite)
        
        return fileOpend.close()
    