import numpy
import random
import copy
import ctypes
import itertools

import const

import ProblemPool


# class cPerceptron(ctypes.Structure):
#     # double calculate(double* dataX, int numInput, double* weights, int* indexes, bool region);
#     _fields_ = [('dataX',ctypes.POINTER(ctypes.c_double)),('numInput',ctypes.c_int),
#                 ('weights',ctypes.POINTER(ctypes.c_double)),('indexes',ctypes.POINTER(ctypes.c_int)),('region',ctypes.c_bool)]
#     def __init__(self,dataX,numInput,weights,indexes,region):        
#         self.numInput = numInput
#         self.region = region
#                  
#         self.dataX = (ctypes.c_double * len(dataX))(*dataX)
#         self.indexes = (ctypes.c_int * len(indexes))(*indexes)
#         self.weights = (ctypes.c_double * len(weights))(*weights)
 
# double calculate(double* dataX, int numInput, double* weights, int* indexes, bool region);
#cPerceptronDLL = ctypes.cdll.LoadLibrary("./cPerceptron.dll")
#cPcCalculate = cPerceptronDLL.calculate
# cPcCalculate.argtypes = [ctypes.POINTER(cPerceptron)]
#cPcCalculate.restype = ctypes.c_double

MIN_NUM_INPUT = const.MIN_NUM_INPUT = 2

def gaussianEleimination(points, indexes):
    
    pointsReducted = []
    for i in range(len(points)):
        pointByIndex = []
        for j in range(len(points[i])):
            if j in indexes:
                pointByIndex.append(points[i][j])
        pointsReducted.append(pointByIndex)
    
    arrA = numpy.array(pointsReducted)
    arrB = numpy.empty(len(points))
    arrB.fill(1.0/(len(points)+1))
    
    for i in range(len(arrA)):
        for j in range(len(arrA[i])):
            if i > j:
                ratio = arrA[i][j]/arrA[j][j]
                
                for k in range(len(arrA[i])):
                    arrA[i][k] -= arrA[j][k]*ratio
                arrB[i] -= arrB[j]*ratio

    for i in range(len(arrA)):        
        for j in range(len(arrA[i])):
            if i < j:
                ratio = arrA[i][j]/arrA[j][j]
                for k in range(j,len(arrA[i])):
                    arrA[i][k] -= arrA[j][k]*ratio
                arrB[i] -= arrB[j]*ratio
                
    weights = []
    for i in range(len(arrB)):
        weights.append( arrB[i] / arrA[i][i]) 
    
    return weights

class PERCEPTRON(object):
    def __init__(self):
        pass
    
    def __copy__(self):
        dest = copy.deepcopy(self)
        return dest

    def initbyNumInput(self,numInput):
        self.threshold = 1.0/(numInput+1)
        self.indexes = []
        self.weights = []
        self.region = bool(random.getrandbits(1))
        
    def initbyPrbPool(self,prbPool):
        numInput = random.randint(MIN_NUM_INPUT,prbPool.sizeX)
        self.threshold = 1.0/(numInput+1)
        self.indexes = sorted(list(random.sample(range(prbPool.sizeX),numInput)))
        self.weights = list(gaussianEleimination(prbPool.getPointsInProblemBox(numInput),self.indexes))
        self.region = bool(random.getrandbits(1))
        
    def __str__(self):
        return str(self.numInput()) +"  " + str(round(self.threshold,2)) + str(self.indexes) + str(self.weights) + str(self.region)
    
    def calculate(self, dataX):
        
        # double calculate(double* dataX, int numInput, double* weights, int* indexes, bool region);
#         cPc = cPerceptron(dataX, self.numInput, self.weights, self.indexes, self.region)        
#         return cPcCalculate(ctypes.byref(cPc))
        
        
        
        
        
       
        total = 0       
          
        for i in range(self.numInput()):
            if (len(self.weights)-1 < i) or (len(dataX)-1 < self.indexes[i]):
                print len(self.weights)-1, i, len(dataX)-1, self.indexes[i]
                print self
                while True:
                    pass
            total += self.weights[i]*dataX[self.indexes[i]]
  
        #step function
#         if (total < self.threshold) == self.region:
#             return 0
#         else:
#             return 1
        
        #Rectifier
        expectedOutput = total - self.threshold + 1.0
        expectedOutput = min(1.0,expectedOutput)
        
        return max(0,expectedOutput)
        
        
    def arrangeIndexes(self,numLayer,stack):
        if numLayer < 0:
            return 0

        for j in range(len(self.indexes)):            
            for i in range(len(stack[numLayer])):
                if self.indexes[j] == stack[numLayer][i]:
                    self.indexes[j] = i
                    break
            
    def checkAdjustTargetPosition(self,numParent,numLayer):
        if numParent < 1:
            return False        
        elif numLayer < 1:
            return False
        
        return True
                
    def adjustIndexesByStack(self,numParent,numLayer,stacks):
        if not self.checkAdjustTargetPosition(numParent, numLayer):
            return False
                    
        return self.adjustIndexesByValue(len(stacks[numParent-1][numLayer-1]))
    
    def adjustIndexesByParents(self,numParent,numLayer,parents):
        if not self.checkAdjustTargetPosition(numParent, numLayer):
            return False
                    
#         if len(parents) < numParent:
#             print "parents out of range: ", numParent
#         else: 
#             if len(parents[numParent-1].layer) < numLayer:
#                 print "layer out of range: ", numLayer
                
        return self.adjustIndexesByValue(len(parents[numParent-1].layer[numLayer-1]))
            
    def adjustIndexesByValue(self,adjustValue):
        for j in range(len(self.indexes)):
            self.indexes[j] += adjustValue
        
        return True
    
    def mutateWeight(self,trash):
        indexMutateWeight = random.randint(0,len(self.weights)-1)
        
        newWeight = random.normalvariate(self.weights[indexMutateWeight],0.1)
        self.weights[indexMutateWeight] = newWeight
        self.inputClear()
        
        return newWeight        
        
    def mutateIndex(self,maxIndex):
        indexMutateIndex = random.randint(0,len(self.indexes)-1)
        
        newIndex = random.randint(0,maxIndex-1)
        self.indexes[indexMutateIndex] = newIndex
        self.inputClear()
        
        return newIndex
    
    def mutateRegion(self,trash):
        self.region = not(self.region)        
        return self.region
        
    def mutate(self,maxIndex):
        menuMutate = {0: self.mutateWeight, 1: self.mutateIndex, 2: self.mutateRegion}
        mutateTarget = random.randint(0,2)
        
        menuMutate[mutateTarget](maxIndex)
        
        return mutateTarget
    
    def inputClear(self):
        newIndexes = sorted(list(set(self.indexes)))
        newWeights = [0.0 for _ in range(len(newIndexes))]
        
        for i, eachIndex in enumerate(self.indexes):
            for j, targetIndex in enumerate(newIndexes):
                if eachIndex == targetIndex:
                    newWeights[j] += self.weights[i]
                    break
                
        self.indexes = newIndexes
        self.weights = newWeights
                
        return self.numInput()
    
    def numInput(self):
        return len(self.indexes) 
    
    def checkIntegrity(self,numData):
        for oneIndex in self.indexes:
            if oneIndex >= numData:
                print self
                return True
        return False
                    
    def isORgate(self):        
        sumANDgateWeights = self.calANDgateValue()*float(self.calOriginalNumInput())        
        return sumANDgateWeights != sum(self.weights)
        
    def calOriginalNumInput(self):
        return int((1.0/self.threshold) - 1.0)
        
    def calANDgateValue(self):
        numInput = float(self.numInput())
        
        if numInput < 2.0:
            return 1.0
        
        return 2.0 / (2.0*(numInput-1)) / (numInput+1)
    
    def isSmallerThan(self,comparedOne):
        srcIndexSet = set(self.indexes)
        compareIndexSet = set(comparedOne.indexes)
        
        if srcIndexSet.issubset(compareIndexSet):
            return not self.isORgate()
        else:
            return comparedOne.isORgate()
                   
        
        
        
        
        
        
                
                    
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")
# pc = PERCEPTRON(prbPool)
# print pc
# print pc.calculate((prbPool.getRandomProblemFromBank())[0])
    
        
        