class LOGGER(object):
    def __init__(self):
        pass
    
    def initLogger(self,nameTestFile,pathBasic="../results/",activate=True):
        self.pathBasic = pathBasic
        self.findPrefixNumber(nameTestFile)
        self.activated = activate

    def writePrefixFile(self,nameTestFile):
        fileOpened = open(self.pathBasic +"_"+ str(self.prefix) + ".txt",'w')
        fileOpened.write(nameTestFile)
        fileOpened.close()
        pass
            
    def findPrefixNumber(self,nameTestFile):
        import os
        
        i = 0
        while os.path.isfile(self.pathBasic +"_"+ str(i) + ".txt"):
            i += 1
        
        self.prefix = i        
        self.writePrefixFile(nameTestFile)
        
        return self.prefix
    
    def getFileName(self,numSimulation,nameCategory,numBlock=-1):
        strName = self.pathBasic +"_"+ str(self.prefix) +"_"+ str(numSimulation) +"_"
        
        if numBlock != -1:
            strName += str(numBlock) + "_" 
            
        strName += nameCategory + ".csv"
        
        return strName
    
    def writeGenerationResult(self,numSimulation,numGeneration,nameCategory,strContent,numBlock=-1):
        if not self.isActivated():
            return False
        
        strFileName = self.getFileName(numSimulation,nameCategory,numBlock) 
        
        if numGeneration != 0:
            modeFile = 'a'
        else:
            modeFile = 'w'
        
        fileOpend = open(strFileName,modeFile)
        
        strWrite = str(numGeneration)+","+strContent+"\n"
        fileOpend.write(strWrite)
        
        return fileOpend.close()
    
    def writeBlockResult(self,numSimulation,nameCategory,strContent,numBlock=-1):
        if not self.isActivated():
            return False
        
        strFileName = self.getFileName(numSimulation,nameCategory,numBlock) 
        
        fileOpend = open(strFileName,'w')
        fileOpend.write(strContent)
        
        return fileOpend.close()
    
    def writeSimulationResult(self,numSimulation,nameCategory,strContent,numBlock=-1):
        if not self.isActivated():
            return False
        
        strFileName = self.getFileName(numSimulation,nameCategory) 
        
        if numBlock > 0:
            modeFile = 'a'
        else:
            modeFile = 'w'
        
        strWrite = str(numBlock) + "," + strContent +"\n"
        
        fileOpend = open(strFileName,modeFile)
        fileOpend.write(strWrite)
        
        return fileOpend.close()
    
    def isActivated(self):        
        return self.activated 
    
    def enable(self):
        self.activated = True
        return True
    
    def disable(self):
        self.activated = False
        return False
    