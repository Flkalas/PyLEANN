import copy
import random

import Sight
import NeuralNetwork

import ProblemPool

class CELL(NeuralNetwork.NEURAL_NETWORK):
    def __str__(self):
        infoStr = "Feeds\n"
        infoStr += str(self.countRight) + " " + str(self.countFeedRate)+ "\n\n"
        
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
        
        self.initSights(prbPool)        
        self.initFeeds(prbPool.sizeY)
        
    def initbyRnas(self, parents, prbPool):
        super(CELL, self).initbyRnas(parents)        
        
        self.initSights(prbPool,self.getSizeLayer())        
        self.initFeeds(prbPool.sizeY)        
        
    def initbyMicevol(self, parents, prbPool):
        super(CELL, self).initbyMicevol(parents)
        
        self.initSights(prbPool,self.getSizeLayer())        
        self.initFeeds(prbPool.sizeY)
    
    def initbyMacevol(self, parents, prbPool):
        super(CELL, self).initbyMacevol(parents)
                
        self.initSights(prbPool,self.getSizeLayer())        
        self.initFeeds(prbPool.sizeY)
        
    def initFeeds(self,sizeY):
        self.feeds = [0 for _ in range(sizeY)]
        self.countFeedRate = [0 for _ in range(sizeY)]
        self.countRight = 0
        
    def initSights(self,prbPool,numLayer=1):
        self.sights = [Sight.SIGHT() for _ in range(prbPool.sizeY)]
        for item in self.sights:
            item.initSight(prbPool,numLayer)
                    
    def solveProblem(self, prb):
        answer = self.calculate(prb[0])
        boolRight = True
        for i in range(len(prb[1])):            
            if self.sights[i].isInSight(prb[0]):
                if answer[i] == prb[1][i]:
                    self.countFeedRate[i] += 1
                else:
                    boolRight = False
            else:
                boolRight = False
                
        if boolRight:
            self.countRight += 1
    
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
            return sum(self.countFeedRate)
        else:
            return self.countFeedRate[indexCount]
        
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
        return self.countRight
    
    def resetAllCounter(self):
        self.countRight = 0
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