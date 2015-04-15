import re
import random

def isFloat(string):
    
    if any(c.isalpha() for c in string):
        return False        
    elif re.match("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",string) is None:
        return False
    else:
        return True

class PROBLEM_POOL(object):
    def __init__(self, nameFile):
        self.createBankFromFile(nameFile)
                
    def createBankFromFile(self,nameFile):
        with open(nameFile) as streamFile:
            totalSize = len(re.split(',| ',streamFile.readline().rstrip('\n')))            
            bank = [[] for _ in range(totalSize)]
        streamFile.close()
        
        with open(nameFile) as streamFile:
            for line in streamFile:
                splitLine = re.split(',| ',line.rstrip('\n'))
                for i in range(totalSize):
                    bank[i].append(splitLine[i])
        streamFile.close()
        
        self.sizeBank = len(bank[0])
        
        #X phase
        self.bankX = []
        for i in range(1,len(bank)):
            self.bankX.append(bank[i])                                
        self.sizeX = len(self.bankX)
                
        self.bankXIsNumerical = [True for _ in range(self.sizeX)]        
        
        #Judge numeric
        for i in range(self.sizeX):
            j = 0
            while self.bankXIsNumerical and (j != len(self.bankX[i])):
                self.bankXIsNumerical[i] &= isFloat(self.bankX[i][j])
                j += 1                
        
#         print self.bankXIsNumerical
#         for i in range(self.sizeX):
#             print self.bankX[i][0]
            
        #Convert to numeric
        self.nameX = []
        for i in range(self.sizeX):
            if self.bankXIsNumerical[i]:
                self.nameX.append([]);
                newBank = []
                for j in range(len(self.bankX[i])):                    
                    newBank.append(float(self.bankX[i][j]))                                               
                self.bankX[i] = newBank
            else:
                setX = list(set(self.bankX[i]))
                tempX = {setX[i] : i for i in range(len(setX))}
                self.nameX.append(tempX)
                newBank = []
                for j in range(len(self.bankX[i])):
                    newBank.append(self.nameX[i][self.bankX[i][j]])
                self.bankX[i] = newBank
                
        #Find range
        self.rangeX = []
        for i in range(self.sizeX):
            if self.bankXIsNumerical[i]:
                self.rangeX.append([min(self.bankX[i]),max(self.bankX[i])])
            else:
                self.rangeX.append([0,len(self.nameX[i])-1])

        #Y phase
        setY = list(set(bank[0]))
        self.nameY = {setY[i] : i for i in range(len(setY))}
        self.sizeY = len(self.nameY)
        self.bankY = [[] for _ in range(self.sizeY)]
        
        for i in range(len(bank[0])):
            classes = 1 << self.nameY[bank[0][i]]            
            for j in range(len(self.bankY)):                
                self.bankY[j].append((classes&(1<<j))>>j)
                
        self.nameY = {v: k for k, v in self.nameY.items()}        
        
        return 0

    def getPointsInProblemBox(self,numPoints):
        points = []
        for _ in range(numPoints):
            points.append(self.getSinglePointsInProblemBox())
        return points
    
    def getSinglePointsInProblemBox(self):
        point = []
        for i in range(len(self.rangeX)):
            point.append(random.uniform(self.rangeX[i][0],self.rangeX[i][1]))
        return point
    
    def getRandomProblemFromBank(self):
        selected = random.randint(0,self.sizeBank-1)
        return self.getOneProblemFromBank(selected)
            
    def getOneProblemFromBank(self,prbIndex):
        prb = []
        
        prbX = []
        for i in range(self.sizeX):
            prbX.append(self.bankX[i][prbIndex])
        prb.append(prbX)

        prbY = []
        for i in range(self.sizeY):
            prbY.append(self.bankY[i][prbIndex])
        prb.append(prbY)
        
        return prb

    def fixCrossValidation(self):
        
     
    
# prbPool = PROBLEM_POOL("./balance.csv")
# print prbPool.getPointsInProblemBox(5)
# print prbPool.getOneProblemFromBank(5)
# print prbPool.getRandomProblemFromBank()



