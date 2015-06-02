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
    def __init__(self):
        pass
                
    def initFromFile(self,nameFile,onCrossValid=False,numBlock=10):
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
            decodeList = self.convertNumToClass(self.nameY[bank[0][i]],self.sizeY)
            for j, eachIndex in enumerate(decodeList):
                self.bankY[j].append(eachIndex)
                
        self.nameY = {v: k for k, v in self.nameY.items()}
        self.normalizer()
        
        if onCrossValid:
            self.fixCrossValidation(numBlock)
        
#         self.printAllBank()
        
        return 0
        
    def convertNumToClass(self,numClass,sizeClasses):
        returnList = []
        numSifted = 1 << numClass
        for j in range(sizeClasses):
            returnList.append((numSifted&(1<<j))>>j)
                
        return returnList

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

    def fixCrossValidation(self,numBlock=10):
        #divide classes
        #self.bankX[i][prbIndex]
        #self.bankY[i][prbIndex]
        import math
        
        newClassBank = [[] for _ in range(self.sizeY)]
        
#         print self.sizeBank
        for i in range(self.sizeBank):
            
            prb = self.getOneProblemFromBank(i)
            for j, onClass in enumerate(prb[1]):
                if onClass == 1:
                    newClassBank[j].append(prb)
        
        #make blocks
        newBlockBank = [[] for _ in range(numBlock)]
        for eachClassBank in newClassBank:
            # under 10 class repeats
            numClassAttr = len(eachClassBank)
            numRepeat = int(math.ceil(float(numBlock)/float(numClassAttr)))
            indexProcess = 0
#             print numRepeat, numClassAttr
            for i in range(numRepeat*numClassAttr):
                newBlockBank[indexProcess%numBlock].append(eachClassBank[indexProcess%numClassAttr])
                indexProcess += 1
                
        #stack each block
        newBanks = []
        newBanks.append([[] for _ in range(self.sizeX)])
        newBanks.append([[] for _ in range(self.sizeY)])
        for eachBlock in newBlockBank:
            for eachAttr in eachBlock:
                for i, eachSection in enumerate(eachAttr):
                    for j, eachValue in enumerate(eachSection):
                        newBanks[i][j].append(eachValue)
        
        self.bankX = newBanks[0]
        self.bankY = newBanks[1]
     
    def printAllBank(self):
        for i in range(self.sizeBank):
            print self.getOneProblemFromBank(i)
            
    def normalizer(self):
        minTarget = -1.0
        maxTarget = 1.0
        
        for i in range(self.sizeX):
            #get max min
            maxBank = max(self.bankX[i])
            minBank = min(self.bankX[i])
#             print maxBank, minBank
            
            if maxBank-minBank == 0:
                self.bankX[i] = [0 for _ in range(len(self.bankX[i]))]
                break
            
            for j, eachItem in enumerate(self.bankX[i]):
                
                self.bankX[i][j] = self.translate(eachItem,minBank,maxBank,minTarget,maxTarget)
                
        self.rangeX = [[minTarget,maxTarget] for _ in range(self.sizeX)]
    
    
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
    
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
    
        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan) 
    
# prbpool = PROBLEM_POOL()
# prbpool.initFromFile("./iris.csv",True)
# prbpool.printAllBank()
# dump = raw_input("view")
# prbpool.normalizer()
# prbpool.printAllBank()
# prbPool.printAllBank()

# print prbPool.getPointsInProblemBox(5)
# print prbPool.getOneProblemFromBank(5)
# print prbPool.getRandomProblemFromBank()



