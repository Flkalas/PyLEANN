import math
import random

import numpy

import ProblemPool

class SIGHT(object):
    def __init__(self):
        pass
    
    def __str__(self):                
        return "Center: " + str(self.center) + " Range: " + str(self.sight)
    
    def initSight(self, prbPool, numLayer):
        if numLayer > 3:
            numLayer = 3         
        
        self.center = prbPool.getSinglePointsInProblemBox()
        
        avgList = []
        for subRange in prbPool.rangeX:
            avgList.append(sum(subRange))
        baseSight = float(sum(avgList)/len(avgList)/3*numLayer)        
        self.sight = abs(random.normalvariate(baseSight,1))
        
        return 0
        
    def isInSight(self,dataX):        
#         return numpy.linalg.norm(numpy.array(dataX)-numpy.array(self.center)) < self.sight
        return self.calDistance(dataX) < self.sight
    
    def moveSightCenter(self):
        pass        
                
    def icrSight(self):
        pass
        
    def calDistance(self,dataX):
        total = 0.0
        for i, singleDimension in enumerate(dataX):
            diff = self.center[i] - singleDimension
            total += diff**2
         
        return math.sqrt(total)
        
        
        
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")
# sight = SIGHT()
# sight.initSight(prbPool,1)
# print sight.center
# print sight.sight
# onepoint = prbPool.getRandomProblemFromBank()
# print onepoint
# print sight.isInSight(onepoint[0])    
