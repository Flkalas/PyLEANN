import copy
import random

import Sight
import NeuralNetwork

import ProblemPool

class CELL(NeuralNetwork.NEURAL_NETWORK):
    def __str__(self):
        infoStr = "Feeds\n"
        infoStr += str(self.countFeedRate)+ "\n\n"
        
        infoStr += "Neural Network\n"
        for i in range(len(self.layer)):
            infoStr += "Layer " + str(i) + "\n"
            for j in range(len(self.layer[i])):
                infoStr += "PC " + str(j) + ": " + str(self.layer[i][j])+"\n"
            infoStr += "\n"
        
        infoStr += "Sights\n"
        for sight in self.sights:
            infoStr += str(sight) +"\n"
        infoStr += "\n"
        
        return infoStr
    
    def __copy__(self):
        dest = copy.deepcopy(self)
        return dest
    
    def initbyPrbpool(self, prbPool):
        super(CELL, self).initbyPrbpool(prbPool)
        
        self.initSightsByProblemPool(prbPool)        
        self.initFeeds(prbPool.sizeY)
        
    def initbyRnas(self, parents):
        self.checkParentsSize(parents)
        
        super(CELL, self).initbyRnas(parents)        
        
        self.initSightsByParents(parents)
        self.initFeeds(len(parents[0].feeds))        
        
    def initbyMicevol(self, parents):
        self.checkParentsSize(parents)
        
        super(CELL, self).initbyMicevol(parents)
        
        self.initSightsByParents(parents)
        self.initFeeds(len(parents[0].feeds))
    
    def initbyMacevol(self, parents):
        self.checkParentsSize(parents)
        
        super(CELL, self).initbyMacevol(parents)
                
        self.initSightsByParents(parents)
        self.initFeeds(len(parents[0].feeds))
        
    def initbyDigest(self,cellHunter,cellPrey):                
        super(CELL, self).initbyDigest(cellHunter,cellPrey)
        
        self.initSightsByParents([cellHunter,cellPrey])
        self.initFeeds(len(cellHunter.feeds))
        
    def initFeeds(self,sizeY):
        self.feeds = [0 for _ in range(sizeY)]
        self.countFeedRate = [0 for _ in range(sizeY+1)]        
        
    def initSightsByProblemPool(self,prbPool,numLayer=1):
        self.sights = [Sight.SIGHT() for _ in range(prbPool.sizeY)]
        for item in self.sights:
            item.initSightByProblemPool(prbPool,numLayer)

    def checkParentsSize(self,parents):
        if len(parents) != 2:
            print "Number of parents must be 2. but it is ", len(parents)
            return False
            
    def initSightsByParents(self,parents):
        sizeLayer = self.getSizeLayer()
                
        self.sights = [Sight.SIGHT() for _ in range(len(parents[0].sights))]
        for i in range(len(self.sights)):
            self.sights[i].initSightByParents(parents,i,sizeLayer)
                    
    def solveProblem(self, prb):
        answer = self.calculate(prb[0])
        boolRight = True
        for i in range(len(prb[1])):            
            if self.sights[i].isInSight(prb[0]):
                #for rectifier
                self.countFeedRate[i+1] += abs(answer[i] - float(prb[1][i]))
                                
                #for step function
#                 if answer[i] == prb[1][i]:
#                     self.countFeedRate[i+1] += 1
#                 else:
#                     boolRight = False
            else:
                boolRight = False
                
                
        if boolRight:
            #for step functoin
#             self.countFeedRate[0] += 1
            
            #for rectifier
            maxIndex = 0
            for i, eachOutput in enumerate(answer):
                if eachOutput > answer[maxIndex]:
                    maxIndex = i
            
            if prb[1][maxIndex] == 1:
                self.countFeedRate[0] += 1            
    
    def gainFeed(self,indexFeed,valFeed):
        self.feeds[indexFeed] += valFeed
        
        return self.feeds[indexFeed]
    
    def metabolicAct(self,multiplier=1):
        self.resetAllCounter()
        self.consumeFeed(multiplier)
        
        for sight in self.sights:
            sight.moveSightCenter()
            sight.icrSight()
        
    def consumeFeed(self,multiplier):
        for i in range(len(self.feeds)):
            self.feeds[i] -= self.getSizeOfAllRef(i)*multiplier
            
        self.processLeverage()
                            
    def processLeverage(self):
        leverage = 0
        debtor = 0
        
        while self.checkHaveDebt():
            for i in range(len(self.feeds)):
                if self.feeds[i] <= 0:                
                    leverage += self.feeds[i]
                    debtor += 1
                    self.feeds[i] = 0
                    
            debtor = len(self.feeds)-debtor
            if debtor < 1:
                return 0        
            leverage = int(leverage/debtor)
            
            for i in range(len(self.feeds)):
                if self.feeds[i] > 0:
                    self.feeds[i] += leverage
                    
    def getCount(self,indexCount=-1):
        if indexCount == -1:
            return sum(self.countFeedRate)-self.countFeedRate[0]
        elif indexCount == -2:
            return sum(self.countFeedRate)
        elif indexCount < len(self.countFeedRate):
            return self.countFeedRate[indexCount] 
        else:
            return 0
        
    def getArrayClassCount(self):
        return self.countFeedRate
        
    def getFeed(self, indexOutput=-1):
        if indexOutput == -1:
            return sum(self.feeds)
        else:
            return self.feeds[indexOutput]
        
    def getCellSize(self):
        sums = 0;
        for i in range(self.getSizeOutput()):
            sums += self.getSizeOfAllRef(i)
        return sums
        
    def getCountRight(self):
        return self.countFeedRate[0]
    
    def resetAllCounter(self):        
        self.countFeedRate = [0 for _ in range(len(self.countFeedRate))]
        
    def checkHaveDebt(self):
        for feed in self.feeds:
            if feed < 0:
                return True
        return False
         
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")
# cell = CELL()
# cell.initbyPrbpool(prbPool)
# for i in range(prbPool.sizeBank):
#     cell.solveProblem(prbPool.getOneProblemFromBank(i))
# print cell
# cell.metabolicAct()
# print cell
# 