import math
import random

import numpy

import ProblemPool

class SIGHT(object):
    def __init__(self):
        pass
    
    def __str__(self):                
        return "Center: " + str(self.center) + " Range: " + str(self.sight)
    
    def initSightByProblemPool(self, prbPool, numLayer):
        if numLayer > 3:
            numLayer = 3         
        
        self.center = prbPool.getSinglePointsInProblemBox()
        
        rangeDimension = []
        avgList = []
        for i in range(prbPool.sizeX):            
            rangeDimension.append(((prbPool.rangeX[i][1] - prbPool.rangeX[i][0])/2.0)**2.2)
            
        baseSight = sum(rangeDimension)**(1.0/2.0)
        baseSight /= 3.0**2
        baseSight *= float(numLayer)**2
        self.sight = abs(random.normalvariate(baseSight,0.3))
        
#         for subRange in prbPool.rangeX:
#             avgList.append(sum(subRange))
#         baseSight = float(sum(avgList)/len(avgList)/3*numLayer)
#         self.sight = abs(random.normalvariate(baseSight,1))
        
        return 0
    
    def initSightByParents(self,parents,index,sizeLayer):
        sightParentSelected = random.choice(parents).sights[index]
        
        self.center = [random.normalvariate(eachAxis,1.0/((sizeLayer+0.1)**1.5)) for eachAxis in sightParentSelected.center]
#         self.center = [random.random()*2.0-1.0 for _ in range(len(sightParentSelected.center))]
        self.sight = random.normalvariate(sightParentSelected.sight,0.1)

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
        
    def getCenterOfTwoPoints(self,points):
        if len(points) != 2:
            return -66
        
        numAxis = len(points[0])
        pointsRotated = [[] for _ in range(numAxis)]
        for eachPoint in points:
            for i, eachAxis in enumerate(eachPoint):
                pointsRotated[i].append(eachAxis)
        
        newPoint = []
        for eachAxis in pointsRotated:            
            newPoint.append(sum(eachAxis)/2.0)
            
        return newPoint
            
            
        
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")
# sight = SIGHT()
# sight.initSightByProblemPool(prbPool,1)
# print sight.center
# print sight.sight
# onepoint = prbPool.getRandomProblemFromBank()
# print onepoint
# print sight.isInSight(onepoint[0])    
