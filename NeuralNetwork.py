import copy
import math
import random
import operator
import itertools

import Rna
import Sight
import Perceptron
import ProblemPool

class NEURAL_NETWORK(object):
    def __init__(self):
        self.layer = []
        pass
        
    def __str__(self):
        infoStr = ""
        for i in range(len(self.layer)):
            infoStr += "Layer " + str(i) + "\n"
            for j in range(len(self.layer[i])):
                infoStr += "PC " + str(j) + ": " + str(self.layer[i][j])+"\n"
            infoStr += "\n"
                
        return infoStr
    
    def __copy__(self):
        dest = copy.deepcopy(self)
        return dest
    
    def initbyPrbpool(self, prbPool):
        initLayer = []
        
        for _ in range(prbPool.sizeY):
            newPC = Perceptron.PERCEPTRON();
            newPC.initbyPrbPool(prbPool) 
            initLayer.append(newPC)
        self.layer.append(initLayer)
        
        return self.checkIntegrity("BASIC")
        
    def initbyRnas(self, parents):
        
        sizeLayer = []        
        for parent in parents:
            sizeLayer.append(parent.getSizeLayer())
                
        targetLayer = random.choice(sizeLayer)
        numOutput = parents[0].getSizeOutput()

        extendedParents = []
        for i, eachLayernum in enumerate(sizeLayer):
            if eachLayernum < targetLayer:
#                 print parents[i]
                extendedParents.append(parents[i].extendLayer(targetLayer))
#                 print extendedParents[i]
            else:
                extendedParents.append(parents[i]) 

        sel = []
        selectedOnes = []
        stacks = [[[] for _ in range(targetLayer-1) ] for _ in range(len(extendedParents))]
        
        for i in range(numOutput):
#             sel.append(random.randint(0,1))
            sel.append(self.randParentByCount(extendedParents, i))                        
            ref = extendedParents[sel[i]].getAllReferenced(i,targetLayer)
            selectedOnes.append(random.choice(ref))

            for j in range(targetLayer-1):
                stacks[sel[i]][j].extend(list(extendedParents[sel[i]].getAllReferenced(selectedOnes[i],j+1,targetLayer)))
                stacks[sel[i]][j] = list(set(stacks[sel[i]][j]))
                
        self.layer = [[] for _ in range(targetLayer-1)]
        
        for i in range(len(stacks)):
            eachStack = stacks[i]
            for j in range(len(eachStack)):
                for indexPerceptron in eachStack[j]:
                    self.layer[j].append(self.createTunedPerceptron(extendedParents[i].layer[j][indexPerceptron], i, j, stacks))
                
        tempLayer = []
        for i in range(numOutput):
            tempLayer.append(self.createTunedPerceptron(extendedParents[sel[i]].layer[targetLayer-1][selectedOnes[i]], sel[i], targetLayer-1, stacks))
        
        if len(tempLayer) > 0:
            self.layer.append(tempLayer)
            
        self.degeneration()
            
        return self.checkIntegrity("RNA")
            
    def checkIntegrity(self,fromWhere="DEFAULT"):        
        for i, eachLayer in enumerate(self.layer):
            if i > 0:
                for eachPerceptron in eachLayer:
                    for eachIndex in eachPerceptron.indexes:
                        if eachIndex > len(self.layer[i-1])-1:
                            print "ERROR: Out of Index in " + fromWhere
                            self.printLayer()
                            while True:
                                pass
                            return False                            
        return True
        
    def checkPerceptronOver(self):
        if len(self.layer) > 1:
            indexSet = []
            for eachPC in self.layer[1]:
                indexSet += eachPC.indexes
            sortedListSet = sorted(list(set(indexSet)), reverse=True)
            
            if len(self.layer[0]) != sortedListSet[0]+1:
                print len(self.layer[0]), sortedListSet[0]
                print "over perceptron"
                self.printLayer()
                return True
                
        return False 
#         if targetLayer > 1:

    def printLayer(self):
        for i, eachL in enumerate(self.layer):
            print i, "layer" 
            for j, eachP in enumerate(eachL):
                print i, j, eachP
            print "layer end"
        print "\n"
                    
    def initbyMicevol(self, parents):
        numLayer = []
        for eachParent in parents:
            numLayer.append(eachParent.getSizeLayer())            
        maxLayer = max(numLayer)
        self.layer = [[] for _ in range(maxLayer-1)]
        
        sizeOutput = parents[0].getSizeOutput()
        
        extendedParents = []
        for eachParent in parents:
            extendedParents.append(eachParent.extendLayer(maxLayer))
            
#         print extendedParents
            
        stacks = [[[]for _ in range(len(extendedParents))] for _ in range(sizeOutput)]
        for i in range(eachParent.getSizeOutput()):
            for j in range(len(extendedParents)):            
                stacks[i][j].extend(extendedParents[j].getAllReferenced(i,maxLayer-1,maxLayer))
                
        for i, eachParent in enumerate(extendedParents):
            for j in range(maxLayer-1):
#                 print eachParent
                for k in range(len(eachParent.layer[j])):
                    newPC = copy.deepcopy(eachParent.layer[j][k])
                    newPC.adjustIndexesByParents(i,j,parents)
                    self.layer[j].append(newPC)
                    
        fuseLayer = [self.createFusingPerceptron(i, stacks, len(extendedParents[0].layer[maxLayer-2])) for i in range(sizeOutput)]
        self.layer.append(fuseLayer)
        
        if self.checkPerceptronOver():
            print len(parents)
            print "Error"
            for eachParent in parents:
                print eachParent
            print "micro"
                        
        self.degeneration()
        
        return self.checkIntegrity("MICRO")
        
    def initbyMacevol(self, parents):
        numBasicLayer = parents[0].getSizeLayer()
        numOutput = parents[0].getSizeOutput()
        
        self.layer = [[] for _ in range(numBasicLayer)]
        
        for i, eachParent in enumerate(parents):
            for j in range(numBasicLayer):
                for k in range(len(eachParent.layer[j])):
                    newPC = copy.deepcopy(eachParent.layer[j][k])
                    newPC.adjustIndexesByParents(i,j,parents)                    
                    self.layer[j].append(newPC)
        
        mergingLayer = [self.createMergingPerceptron(i, numOutput) for i in range(numOutput)]
        self.layer.append(mergingLayer)

        if self.checkPerceptronOver():
            print "Error"
            for eachParent in parents:
                print eachParent
                            
            print "macro"
        
        self.degeneration()
        
        return self.checkIntegrity("MACRO")

    def calculate(self, dataX):        
        outputData = dataX
        for i in range(len(self.layer)):
            inputData = outputData
            outputData = []
            for j in range(len(self.layer[i])):
                for oneIndex in self.layer[i][j].indexes:
                    if oneIndex >= len(inputData):
                        print "out of index"
                        print id(self)
                        print self
                        print "one"
                        print self.layer[i][j]
                        print "ERORR"
                        while True:
                            pass
#                     if len(self.layer[i][j].indexes) <= 1:                        
#                         print "zero Peceptron"
#                         print id(self)
#                         print self
                    
                
                    
                outputData.append(self.layer[i][j].calculate(inputData))
        return outputData
    
    def mutate(self,sizeX):        
        indexMutatePerceptron = random.randint(0,len(self.layer[0])-1)        
#         if len(self.layer[numMutateLayer][indexMutatePerceptron].indexes)-1 <= 0 or len(self.layer[numMutateLayer][indexMutatePerceptron].weights) <= 1:
#             print self
        self.layer[0][indexMutatePerceptron].mutate(sizeX)
        
        return self.checkIntegrity("MUTATE")
    
    def degeneration(self):
        if self.getSizeLayer() < 2:
            return False
        
#         self.printLayer()
        self.degenSimilarity()
        self.degenUniquness()
        self.degenLayer()
        
        
                
    def degenSimilarity(self):
        listSimilarity = []
        
        for compareSet in itertools.combinations(range(len(self.layer[0])),2):
            compareSet = list(compareSet)
            if self.isSimilar(compareSet):
                listSimilarity.append(list(compareSet))

        if len(listSimilarity) == 0:
            return False
    
        listSimilarityPC = self.getCliqueSetCombinedList(listSimilarity,len(self.layer[0]))
        
        deletedPClist = [] 
        for eachSet in listSimilarityPC:                        
            choosedOne = random.choice(eachSet)
            eachSet.remove(choosedOne)
            
            self.replaceIndex(1, eachSet, choosedOne)
            
            deletedPClist += eachSet
            
        deletedPClist.sort(reverse=True)
            
        self.adjustIndexByDelete(1, deletedPClist)
        self.deletePerceptrons(0, deletedPClist)
                        
        return len(listSimilarity) > 0
    
    def degenUniquness(self):        
        if self.getSizeLayer() < 3:
            return False
        
        for i in range(1,len(self.layer)-1):            
            listUniquness = []
            
            for compareSet in itertools.combinations(range(len(self.layer[i])),2):
                if not self.isUnique(compareSet,i):
                    listUniquness.append(list(compareSet))

            if len(listUniquness) == 0:
                return False
            
            listNotUniquePC = self.getCliqueSetCombinedList(listUniquness,len(self.layer[i]))
            
            listDeletedPC= []
            for eachNotUnique in listNotUniquePC:
                smallestOne = self.getSmallestOne(eachNotUnique,i)
                eachNotUnique.remove(smallestOne)
                
                self.replaceIndex(i+1, eachNotUnique, smallestOne)
                
                listDeletedPC += eachNotUnique
            
            listDeletedPC.sort(reverse=True)
            self.adjustIndexByDelete(i+1, listDeletedPC)            
            
            self.deletePerceptrons(i, listDeletedPC)
        
        return len(listDeletedPC) > 0
    
    def degenLayer(self):
        if self.getSizeLayer() < 2:
            return False
        
        prevSizeLayer = self.getSizeLayer()
        
        for i in reversed(range(1,self.getSizeLayer())):
            setIndex = set()
            for eachPerceptron in self.layer[i]:
                if len(eachPerceptron.indexes) != 1:
                    break
                else:
                    setIndex.add(eachPerceptron.indexes[0])
                    
            if (list(setIndex) == range(len(self.layer[i]))) and (len(self.layer[i]) == len(self.layer[i-1])):
                
#                 print "Layer------------------------------------------"
#                 self.printLayer()
#                 
#                 print "\n"
#                 for eachPerceptron in self.layer[i]:
#                     print eachPerceptron
#                 print "\n"
#                 for eachPerceptron in self.layer[i-1]:
#                     print eachPerceptron
                    
                newLayer = []
                for eachPerceptron in self.layer[i]:                    
                    newLayer.append(self.layer[i-1][eachPerceptron.indexes[0]])
                
                self.layer = self.layer[0:i]
                self.layer[i-1] = newLayer
        
#                 print "\n"
#                 for eachPerceptron in newLayer:
#                     print eachPerceptron
#                 print "\n"
#                     
#                 self.printLayer()

        return prevSizeLayer != self.getSizeLayer()
        
    def getSmallestOne(self,listNotUnique,indexLayer):
        smallest = listNotUnique[0]
        
        for eachIndex in listNotUnique[1:]:
            if self.layer[indexLayer][eachIndex].isSmallerThan(self.layer[indexLayer][smallest]):
                smallest = eachIndex
        
        return smallest    
            
    def getCliqueSetCombinedList(self,listToFindClique,sizeLayer):
        if len(listToFindClique) < 3:
            return listToFindClique
        
        def getCliquesN(adMat,sizeClique):            
            if sizeClique < 3:
                return []
            
            n = len(adMat)
            
            listClique3 = []
            
            for i in range(n):
                firstConnected = [j for j in range(i+1,n) if adMat[i][j]]
                for compareSet in itertools.combinations(firstConnected,2):
                    compareSet = list(compareSet)
                    if adMat[compareSet[0]][compareSet[1]]:
                        compareSet.append(i)
                        listClique3.append(sorted(compareSet))
                
            if sizeClique < 4:
                return listClique3
            
            listCliqueN = [listClique3]
                        
            for i in range(sizeClique-3):
                hasLargerClique = [False for _ in range(len(listCliqueN[i]))]
                listLargerClique = []                
                
                for j, eachClique in enumerate(listCliqueN[i]):
                    for k in range(eachClique[i+2]+1,n):                        
                        isLarger = True
                                                
                        for eachIndex in eachClique:                    
                            if not adMat[eachIndex][k]:
                                isLarger = False                        
                                break
                            
                        if isLarger:
                            largerClique = copy.deepcopy(eachClique)
                            largerClique.append(k)
                            listLargerClique.append(sorted(largerClique))
        
                if len(listLargerClique) > 0:
                    listCliqueN.append(listLargerClique)
                else:
                    break
                        
                for largerClique in listLargerClique:
                    for setLowerClique in itertools.combinations(largerClique,i+3):
                        for j, eachClique in enumerate(listCliqueN[i]):                    
                            if list(setLowerClique) == eachClique:
                                hasLargerClique[j] = True
                                break
                
                newListCliqueN = []
                for j, eachDelete in enumerate(hasLargerClique):
                    print listCliqueN[i], hasLargerClique
                    if not eachDelete:
                        newListCliqueN.append(listCliqueN[i][j])
                listCliqueN[i] = newListCliqueN
            
            listMergingCluque = []
            for eachCliqueN in listCliqueN:
                for eachClique in eachCliqueN:
                    listMergingCluque.append(eachClique)
                        
            return listMergingCluque
             
        adMat = [[False for _ in range(sizeLayer)] for _ in range(sizeLayer)]
        
        for eachlistToFindClique in listToFindClique:
            adMat[eachlistToFindClique[0]][eachlistToFindClique[1]] = True
            adMat[eachlistToFindClique[1]][eachlistToFindClique[0]] = True

        listClique = getCliquesN(adMat,sizeLayer)
        
        for eachClique in listClique:
            for eachConnection in itertools.combinations(eachClique,2):
                eachConnection = list(eachConnection)
                adMat[eachConnection[0]][eachConnection[1]] = False
                adMat[eachConnection[1]][eachConnection[0]] = False
        
        for posMat in itertools.combinations(range(sizeLayer),2):
            posMat = list(posMat)
            if adMat[posMat[0]][posMat[1]]:  
                listClique.append([posMat[0],posMat[1]])
        
        return listClique
    
    def insertToSet(self,setList,testSet):
        isNotExist = True
        numInserted = 0
        
        setNextLists = []

        for singleIndex in testSet:            
            for i, singleSet in enumerate(setList):
                if singleIndex in singleSet:
                    tempList = copy.deepcopy(singleSet)
                    tempList += testSet
                    isNotExist = False
                    break
                 
        
            
                    print "TEST", testSet
                    print "SET", setList
                    
                    setList[i] += testSet
                    numInserted += 1
                    print numInserted
                    isNotExist = False

                    

        if numInserted > 1:
            print "SET", setList
            def clearDuplicateSet(setList):
                setNewLists = []
                for i, listBased in enumerate(setList):
                    for j, listTargeted in enumerate(setList):
                        if i != j:
                            for eachIndex in listBased:
                                if eachIndex in listTargeted:
                                    listNew = listBased+listTargeted
                                    setList.append(listNew)
                                    setList.remove(listBased)
                                    setList.remove(listTargeted)                                    
                                    break
            clearDuplicateSet(setList)
            print "RESULT", setList
            while True:
                pass
            
        if isNotExist:
            setList.append(testSet)

        return not isNotExist
    
    def isSimilar(self,pcIndexes):
        pcSet = []
        for singleIndex in pcIndexes:
            pcSet.append(self.layer[0][singleIndex])
            
        if pcSet[0].region != pcSet[1].region:
            return False
        
        if not self.isSameInput(pcSet):
            return False
               
        degree = self.calDegreeBetweenPerceptron(pcSet)
#         print degree
        compareKeyValue = math.sqrt(math.sin(degree))*5
        
        return compareKeyValue < random.random()
    
    def isSameInput(self,pcSet):        
#         print pcSet, sorted(list(set(pcSet[0].indexes))), sorted(list(set(pcSet[1].indexes)))
        return cmp(sorted(list(set(pcSet[0].indexes))),sorted(list(set(pcSet[1].indexes)))) == 0
        
    def calDegreeBetweenPerceptron(self,pcSet):
        if len(pcSet) != 2:
            return -1
        
        vectors = [dict((pcSet[i].indexes[j],pcSet[i].weights[j]) for j in range(pcSet[i].numInput())) for i in range(len(pcSet))]
        
#         print vectors        
        
        if len(set(vectors[0].items())^set(vectors[1].items())) == 0:
            return 0
            
        vectorInnerProduct = 0.0;
        for key in vectors[0].keys():
            vectorComponentProduction = 1.0
            for eachVector in vectors:
                vectorComponentProduction *= eachVector[key]
            vectorInnerProduct += vectorComponentProduction
        
        vectorsLength = []
        
        for eachVector in vectors:
            singleVectorLength = sum(value**2 for value in eachVector.values())
            vectorsLength.append(math.sqrt(singleVectorLength))
        
        vectorsLengthProduct = reduce(operator.mul, vectorsLength, 1)
        
        degree = math.acos(vectorInnerProduct/vectorsLengthProduct)
        
        return min(degree, math.pi-degree)
    
    
    def replaceIndex(self,indexTargetLayer,listDuplicatedPC,indexReplace):
        for i in range(len(self.layer[indexTargetLayer])):
            self.layer[indexTargetLayer][i].indexes = [singleIndex if singleIndex not in listDuplicatedPC else indexReplace for singleIndex in self.layer[indexTargetLayer][i].indexes]
        
        return True
            
    def adjustIndexByDelete(self,indexTargetLayer,listDeleteIndex):
        for eachDeletedIndex in listDeleteIndex:        
            for i, eachPC in enumerate(self.layer[indexTargetLayer]):
                for j, eachPcIndex in enumerate(eachPC.indexes):                    
                    if eachPcIndex > eachDeletedIndex:
                        self.layer[indexTargetLayer][i].indexes[j] -= 1                        
                self.layer[indexTargetLayer][i].inputClear()
                
        return True
                        
    def deletePerceptrons(self,indexLayer,listDeletedPcIndexes):
        newLayer = []
        
        for i, eachPC in enumerate(self.layer[indexLayer]):
            if i not in listDeletedPcIndexes:
                newLayer.append(eachPC)
                
        self.layer[indexLayer] = newLayer
            
        return len(listDeletedPcIndexes)
            
    def isUnique(self,compareSet,indexLayer):        
        
        if self.layer[indexLayer][0].region != self.layer[indexLayer][1].region:
            return True
        
        if self.isFrontSmaller(compareSet,indexLayer):
            smaller = 0
            larger = 1
        else:
            smaller = 1
            larger = 0
        
        pcSet = []
        for eachIndex in compareSet:
            pcSet.append(self.layer[indexLayer][eachIndex])
            
        if not set(pcSet[smaller].indexes).issubset(set(pcSet[larger].indexes)):
            return True
        
        if not pcSet[larger].isORgate():
            temp = smaller
            smaller = larger
            larger = temp
        
        setReferencedInNextLayer = []  
        listFirstOneReference = []
        for eachPC in pcSet:
            ref = []
            indexPCinTargetLayer = self.layer[indexLayer].index(eachPC)
            
            for i, eachPCinNextLayer in enumerate(self.layer[indexLayer+1]):
                if indexPCinTargetLayer in eachPCinNextLayer.indexes:
                    ref.append(i) 
            
            setReferencedInNextLayer.append(set(ref))
            listFirstOneReference.append(ref[0])
            
        for eachSet in setReferencedInNextLayer:
            if not self.isArrSameGate(eachSet, indexLayer):
                return True
        
        if self.layer[indexLayer][listFirstOneReference[0]].isORgate() != self.layer[indexLayer][listFirstOneReference[1]].isORgate():
            return True 
        
        if not setReferencedInNextLayer[smaller].issubset(setReferencedInNextLayer[larger]):
            return True
    
        return False
    
    def isFrontSmaller(self,compareSet,indexLayer):
        return self.layer[indexLayer][compareSet[0]].numInput() < self.layer[indexLayer][compareSet[1]].numInput()
    
    def isArrSameGate(self,refSet,indexLayer=-1):
        if indexLayer < 0:
            return False
                
        refSet = list(refSet)        
        firstOne = self.layer[indexLayer][refSet[0]].isORgate()
        
        for eachIndex in refSet:
            if self.layer[indexLayer][eachIndex].isORgate() != firstOne:
                return False
        
        return True
    
    def extendLayer(self,numTargetLayer):
        if numTargetLayer == self.getSizeLayer():
            return copy.deepcopy(self)        

        extendedNN = copy.deepcopy(self)
        
        for _ in range(self.getSizeLayer(),numTargetLayer):
            passingLayer = [self.createPassingPerceptron(i) for i in range(extendedNN.getSizeOutput())]
            extendedNN.layer.append(passingLayer)
            
        return extendedNN
            
    def createPassingPerceptron(self,indexOutput):
        passingPC = Perceptron.PERCEPTRON()
        passingPC.initbyNumInput(1)
        passingPC.indexes.append(indexOutput)
        passingPC.weights.append(1.0)
        passingPC.region = True
        
        return passingPC
    
    def createMergingPerceptron(self,indexOutput,numOutput):
        mergingPC = Perceptron.PERCEPTRON()
        
        numInput = 2
        weightAndMerging = self.randMergingWeight()
                
        mergingPC.initbyNumInput(numInput)
        mergingPC.indexes = [indexOutput+numOutput*i for i in range(numInput)]
        mergingPC.weights = [weightAndMerging for _ in range(numInput)]
        mergingPC.region = True
        
        return mergingPC
    
    def randMergingWeight(self):
        if random.randint(0,1) == 0:
            return 2.0/9.0 #AND
        else:
            return 2.0/3.0 #OR   

    def createTunedPerceptron(self,srcPerceptron,numParent,numLayer,stacks):
        copyPerceptron = copy.deepcopy(srcPerceptron)
        copyPerceptron.arrangeIndexes(numLayer-1,stacks[numParent])
        copyPerceptron.adjustIndexesByStack(numParent,numLayer,stacks)
        
        return copyPerceptron
    
    def createFusingPerceptron(self,indexOutput,stacks,sizePreLayer):
        fusingPC = Perceptron.PERCEPTRON()
        
        numInput = sum([len(eachParentRef) for eachParentRef in stacks[indexOutput]])
        weightToFuse = self.calPeceptronWeight(numInput)
        
        fusingPC.initbyNumInput(numInput)
        fusingPC.weights = [weightToFuse for _ in range(numInput)]
        for i, eachParentRef in enumerate(stacks[indexOutput]):
            for eachRef in eachParentRef:
                fusingPC.indexes.append(eachRef+i*sizePreLayer)
        fusingPC.region = True
        
        return fusingPC
    
    def calPeceptronWeight(self,numInput):
        
        def calORgateValue(numInput):
            return 2.0 / float(numInput+1)
    
        def calANDgateValue(numInput):
            return 2.0 / (2.0*float(numInput-1)) / (float(numInput)+1)
        
        if random.random() < 0.5:
            return calANDgateValue(numInput)
        else:
            return calORgateValue(numInput)
    
    def getRefStructure(self,numOutput):
        if self.checkIndexInLayer(numOutput):
            return []
    
    def getAllReferenced(self,indexInLayer,numTargetLayer=1,numLayer=-1):
        if self.checkIndexInLayer(indexInLayer,numLayer):
            return []
        
        if self.checkLayer(numTargetLayer):

            return []
        
        if numLayer == -1:
            numLayer = len(self.layer)
        
        inputs = [indexInLayer]
        outputs = []
        for i in reversed(range(numTargetLayer,numLayer)):
            for j in inputs:
                for k in range(self.layer[i][j].numInput()):
                    outputs.append(self.layer[i][j].indexes[k])
            inputs = list(set(outputs))
            outputs = []            
        
        return inputs
    
    def getSizeOfAllRef(self, numOutput):
        if self.checkIndexInLayer(numOutput):
            return []
                
        sizeOutput = 0
        
        inputs = [numOutput]
        sizeOutput += len(inputs)
        outputs = []
        i = len(self.layer)-1
        while i > 0:
            for j in inputs:
                for k in range(self.layer[i][j].numInput()):
                    outputs.append(self.layer[i][j].indexes[k])
                        
            inputs = list(set(outputs))
            sizeOutput += len(inputs)
            outputs = []
            i -= 1
        
        return sizeOutput
        
    def getInputAxisOfDimension(self, numOutput):
        refList = self.getAllReferenced(numOutput)
        
        axisDimension = []
        for idx in refList:
            for i in self.layer[0][idx].indexes:
                axisDimension.append(i)
        
        return list(set(axisDimension))
    
    def getSizeLayer(self):
        return len(self.layer)
    
    def getSizeOutput(self):
        return len(self.layer[len(self.layer)-1])
    
    def randParentByCount(self,parents,indexCount):
        counts = []
        for eachParent in parents:
            counts.append(eachParent.getCount(indexCount))
        
        sel = random.randint(0,sum(counts)+1)
        
#         if parents[0].getSizeLayer() > 1:
#             print sel, counts
        
        if sel < counts[0]+1:
            return 0
        else:
            return 1
        
    def checkIndexInLayer(self,IndexInLayer,numLayer=-1):        
        if numLayer == -1:
            numLayer = len(self.layer)
                    
        if not self.checkLayer(numLayer):
            return (IndexInLayer < 0) or (IndexInLayer > len(self.layer[numLayer-1])-1)
        else:
            return True
        
    def checkLayer(self,numLayer):
        if numLayer > len(self.layer) or numLayer < 1:
            return True
        else:
            return False
    
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")  
# nn = NEURAL_NETWORK()
# nn.initbyPrbpool(prbPool)
# print nn
# print nn.calculate(prbPool.getRandomProblemFromBank()[0])
# newlayer = []
#     
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(2)
# newpc.indexes.append(0)
# newpc.indexes.append(1)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#     
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(1)
# newpc.indexes.append(2)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#     
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(3)
# newpc.indexes.append(0)
# newpc.indexes.append(1)
# newpc.indexes.append(2)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#     
# nn.layer.append(newlayer)
#      
# newlayer = []
#      
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(1)
# newpc.indexes.append(0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#      
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(2)
# newpc.indexes.append(0)
# newpc.indexes.append(1)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#      
# newpc = Perceptron.PERCEPTRON()
# newpc.initbyNumInput(3)
# newpc.indexes.append(0)
# newpc.indexes.append(1)
# newpc.indexes.append(2)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newpc.weights.append(2.0/3.0)
# newlayer.append(newpc)
#      
# nn.layer.append(newlayer)
#     
# print len(nn.layer[len(nn.layer)-1])-1
# print nn.getAllReferenced(0,3,2)
# print nn.getAllReferenced(1,3,2)
# print nn.getAllReferenced(2,3,2)
# print nn.getAllReferenced(0,2)
# print nn.getAllReferenced(1,2)
# print nn.getAllReferenced(2,2)
# print nn.getAllReferenced(0,1)
# print nn.getAllReferenced(1,1)
# print nn.getAllReferenced(2,1)
# print nn.getAllReferenced(0,2,1)
# print nn.getAllReferenced(1,2,1)
# print nn.getAllReferenced(2,2,1)
# print nn.getAllReferenced(0,1,1)
# print nn.getAllReferenced(1,1,1)
# print nn.getAllReferenced(2,1,1)
# print nn.getAllReferenced(0,3,3)
# print nn.getAllReferenced(1,3,3)
# print nn.getAllReferenced(2,3,3)
# print nn.getAllReferenced(0,2,3)
# print nn.getAllReferenced(1,2,3)
# print nn.getAllReferenced(2,2,3)
# print nn.getAllReferenced(0,1,3)
# print nn.getAllReferenced(1,1,3)
# print nn.getAllReferenced(2,1,3)
# print nn.getSizeOfAllRef(0)
# print nn.getSizeOfAllRef(1)
# print nn.getSizeOfAllRef(2)
# 
# print "*****************************"
# rna = nn.getRna(0,3)
# for i in range(len(rna)):
#     print i
#     for eachrna in rna[i]:  
#         for each in eachrna:
#             print each
#         print ""
#     print "-------------------"
# print "*****************************"
# 
# rna = nn.getRna(1,1)
# for i in range(len(rna)):
#     print i
#     for eachrna in rna[i]:        
#         for each in eachrna:
#             print each
#         print ""
#     print "-------------------"
# print "*****************************"
# 
# rna = nn.getRna(2,3)
# for i in range(len(rna)):
#     print i
#     for eachrna in rna[i]:
#         for each in eachrna:
#             print each
#         print ""
#     print "-------------------"    
# print "*****************************"
# 
# 
# rna = nn.getRna(2,2)
# for i in range(len(rna)):
#     print i
#     for eachrna in rna[i]:
#         for each in eachrna:
#             print each
#         print ""
#     print "-------------------"
# print "*****************************"
#         