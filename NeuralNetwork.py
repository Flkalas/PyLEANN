import copy
import math
import random
import operator
import itertools

import Perceptron
import quine_mccluskey.qm
qmActor = quine_mccluskey.qm.QuineMcCluskey()

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
        
        return self.checkIntegrity(prbPool.sizeY,"BASIC")
        
    def initbyRnas(self, parents):
        
#         print parents
        
        sizeLayer = []        
        for parent in parents:
            sizeLayer.append(parent.getSizeLayer())
                
        targetLayer = random.choice(sizeLayer)
        numOutput = parents[0].getSizeOutput()
        numRealOutput  = min([eachParent.getSizeOutput() for eachParent in parents])

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
            sel.append(self.randParentByCount(parents, i))
            ref = extendedParents[sel[i]].getAllReferenced(i,targetLayer)
            if len(ref) < 1:
                print parents
                for each in parents:
                    print each
                print "extened"    
                print extendedParents
                for each in extendedParents:
                    print each                
                print ref
                print i, sel[i], targetLayer
            
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
            
        return self.checkIntegrity(numRealOutput,"RNA")
            
    def checkIntegrity(self,numBaseOutput,fromWhere="DEFAULT"):        
        if self.getSizeOutput() != numBaseOutput:
            print "Self: ", self.getSizeOutput(), ", Parents: ", numBaseOutput, fromWhere
            while True:
                pass

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
        numRealOutput  = min([eachParent.getSizeOutput() for eachParent in parents])
        
        extendedParents = []
        for eachParent in parents:
            extendedParents.append(eachParent.extendLayer(maxLayer))
            
#         print extendedParents
            
        stacks = [[[]for _ in range(len(extendedParents))] for _ in range(sizeOutput)]
        for i in range(sizeOutput):
            for j in range(len(extendedParents)):
                if len(stacks) <= i or len(stacks[i]) <= j:                    
                    print extendedParents
                    print stacks                    
                    print sizeOutput, i, j
                
                stacks[i][j].extend(extendedParents[j].getAllReferenced(i,maxLayer-1,maxLayer))
                
        for i, eachParent in enumerate(extendedParents):
            for j in range(maxLayer-1):
#                 print eachParent
                for k in range(len(eachParent.layer[j])):
                    newPC = copy.deepcopy(eachParent.layer[j][k])                    
                    newPC.adjustIndexesByParents(i,j,extendedParents)
                    self.layer[j].append(newPC)
                    
        fuseLayer = [self.createFusingPerceptron(i, stacks, len(extendedParents[0].layer[maxLayer-2])) for i in range(sizeOutput)]
        self.layer.append(fuseLayer)
        
        self.degeneration()
        
        return self.checkIntegrity(numRealOutput,"MICRO")
        
    def initbyMacevol(self, parents):
        numBasicLayer = parents[0].getSizeLayer()
        numOutput = parents[0].getSizeOutput()
        numRealOutput  = min([eachParent.getSizeOutput() for eachParent in parents])
        
        numLayer = []
        for eachParent in parents:
            numLayer.append(eachParent.getSizeLayer())
        maxLayer = max(numLayer)        
        
        extendedParents = []
        for eachParent in parents:
            extendedParents.append(eachParent.extendLayer(maxLayer))
                
        self.layer = [[] for _ in range(numBasicLayer)]
        
        for i, eachParent in enumerate(extendedParents):
            for j in range(numBasicLayer):
                for k in range(len(eachParent.layer[j])):
                    newPC = copy.deepcopy(eachParent.layer[j][k])
                    newPC.adjustIndexesByParents(i,j,extendedParents)                    
                    self.layer[j].append(newPC)
        
        mergingLayer = [self.createMergingPerceptron(i, numOutput) for i in range(numOutput)]
        self.layer.append(mergingLayer)
        
        self.degeneration()
        
        return self.checkIntegrity(numRealOutput,"MACRO")
    
    def initbyDigest(self,cellHunter,cellPrey):
        pass

    def calculate(self, dataX, indexStartLayer=0, mode=0):        
        outputData = dataX
        for i in range(indexStartLayer, len(self.layer)):
            inputData = outputData
            outputData = []
            for j in range(len(self.layer[i])):
#                 for oneIndex in self.layer[i][j].indexes:
#                     if oneIndex >= len(inputData):
#                         print "out of index"
#                         print id(self)
#                         print self
#                         print "one"
#                         print self.layer[i][j]
#                         print "ERORR"
#                         while True:
#                             pass
#                     if len(self.layer[i][j].indexes) <= 1:                        
#                         print "zero Peceptron"
#                         print id(self)
#                         print self
                outputData.append(self.layer[i][j].calculate(inputData,mode))
        return outputData
    
    def mutate(self,sizeX):
        numPrevOutput = self.getSizeOutput()
        indexMutatePerceptron = random.randint(0,len(self.layer[0])-1)        
#         if len(self.layer[numMutateLayer][indexMutatePerceptron].indexes)-1 <= 0 or len(self.layer[numMutateLayer][indexMutatePerceptron].weights) <= 1:
#             print self
        self.layer[0][indexMutatePerceptron].mutate(sizeX)
        
        return self.checkIntegrity(numPrevOutput,"MUTATE")
    
    def degeneration(self):
        if self.getSizeLayer() < 2:
            return False
        
#         self.printLayer()
        self.degenSimilarity()
        self.degenQMalgorithm()
        self.degenLayer()
#         self.degenUniquness()
        
        
    def mergeConnectedGraph(self,listSetSimilarity):            
        numConfirm = 0
        listToNext = listSetSimilarity
        
        while numConfirm != len(listToNext):
            listToMerge = listToNext
            listToNext = []
            numConfirm = 0

            waitSetList = [True for _ in range(len(listToMerge))]
            
            for i,setBased in enumerate(listToMerge):
                for j, setTargeted in enumerate(listToMerge):
                    if waitSetList[i] and waitSetList[j] and i != j:
                        if len(setTargeted & setBased) > 0:
                            listToNext.append(setTargeted|setBased)
                            waitSetList[i] = False
                            waitSetList[j] = False
                            break
                if waitSetList[i]:
                    listToNext.append(setBased)
                    waitSetList[i] = False
                    numConfirm += 1
        
        listSimilar = [list(eachItem) for eachItem in listToNext]
                    
        return listSimilar
    
    def degenSimilarity(self):        
        listSetSimilarity = []
        
        for compareSet in itertools.combinations(range(len(self.layer[0])),2):
            compareSet = list(compareSet)
            if self.isSimilar(compareSet):
                listSetSimilarity.append(set(compareSet))

        if len(listSetSimilarity) == 0:
            return False
        
        numPrevOutput = self.getSizeOutput()
        listSimilarityPC = self.mergeConnectedGraph(listSetSimilarity)
        
        #temp
#         listsSimilar = [list(eachItem) for eachItem in listSetSimilarity]
#         print listsSimilar
#         print listSimilarityPC
#         listCilquePC =  self.getCliqueSetCombinedList(listsSimilar, len(self.layer[0]))
#         
#         if len(listCilquePC) != len(listSimilarityPC):
#             print listCilquePC
#             print "not same"
#         while len(listCilquePC) != len(listSimilarityPC):
#             pass
        #temp end
        
        deletedPClist = [] 
        for eachSet in listSimilarityPC:                        
            choosedOne = random.choice(eachSet)
            eachSet.remove(choosedOne)
            
            self.replaceIndex(1, eachSet, choosedOne)
            
            deletedPClist += eachSet
            
        deletedPClist.sort(reverse=True)
#         print deletedPClist
            
        self.adjustIndexByDelete(1, deletedPClist)
        self.deletePerceptrons(0, deletedPClist)

        self.checkIntegrity(numPrevOutput,"Degen Similarity")

        return len(listSetSimilarity) > 0
    
    
    def degenQMalgorithm(self):
        

        listOptimizedOutput = []
        listIsOneLayer = [False for _ in range(self.getSizeOutput())]
        for outputIndex in range(self.getSizeOutput()):
            listAllRef = self.getAllReferenced(outputIndex)            
            numZeroPendding = len(self.layer[0])
            baseInput = [0 for _ in range(numZeroPendding)]
                        
            ones = []                        
            for sizeSet in range(len(listAllRef)+1):
                for subSet in itertools.combinations(listAllRef,sizeSet):
                    testInput = copy.deepcopy(baseInput)
                    listSubset = list(subSet)
                    for eachInput in listSubset:
                        testInput[eachInput] = 1
                        
                    testOutput = self.calculate(testInput, 1, 1)                        
                    if testOutput[outputIndex] == 1:
                        strBinary = ""
                        for eachIndex in testInput:
                            strBinary = str(eachIndex)+strBinary
                        numberOne = int(strBinary,2)
                        ones.append(numberOne)                        
            
            qmResult = list(qmActor.simplify(ones))            
            
            listIsPassing = [False for _ in range(len(qmResult))]
            listANDgates = []
            for i, eachResult in enumerate(qmResult):
                eachResult = eachResult[::-1]                
                cnt = eachResult.count('1')
                
                if cnt == 1:
                    listIsPassing[i] = True
                
                inputsAND = []
                prevPosition  = 0
                for _ in range(cnt):
                    nowPosition = eachResult.find('1',prevPosition)
                    inputsAND.append(nowPosition)
                    prevPosition = nowPosition+1
                
                listANDgates.append(inputsAND)

            listIsOneLayer[outputIndex] = all(listIsPassing) or (len(listANDgates)==1)
            listOptimizedOutput.append(listANDgates)

        #Gen new layer
        newLayers = []
        if all(listIsOneLayer):
            newLayer = []
            for eachOutput in listOptimizedOutput:
                newPerceptron = Perceptron.PERCEPTRON()
                if len(eachOutput) == 1:
                    newPerceptron.initbyANDgateList(eachOutput[0])
                else:                    
                    reducedList = reduce(operator.add, eachOutput)
                    newPerceptron.initbyORgateList(reducedList)                    
                newLayer.append(newPerceptron)
                
            newLayers.append(newLayer)
        else:
            #unique list of list            
            setANDgate = set()
            for eachOutput in listOptimizedOutput:
                for eachANDindexes in eachOutput:
                    setANDgate.add(tuple(eachANDindexes))
            uniqueANDindexes = [list(indexesAND) for indexesAND in setANDgate]            
            
            #AND LAYER
            newANDLayer = []
            for eachANDindexes in uniqueANDindexes:
                newPerceptron = Perceptron.PERCEPTRON()
                newPerceptron.initbyANDgateList(eachANDindexes)
                newANDLayer.append(newPerceptron)
            newLayers.append(newANDLayer)
                        
            #OR LAYER
            newORLayer = []
            for eachOutput in listOptimizedOutput:
                indexesOR = []
                for eachANDindexes in eachOutput:
                    for i, eachLayerIndexes in enumerate(uniqueANDindexes):
                        if set(eachANDindexes) == set(eachLayerIndexes):
                            indexesOR.append(i)
                            break
                
                newPerceptron = Perceptron.PERCEPTRON()
                newPerceptron.initbyORgateList(indexesOR)
                newORLayer.append(newPerceptron)                
            newLayers.append(newORLayer)
        
        self.layer = [self.layer[0]]
        self.layer.extend(newLayers)
        
        return len(self.layer)
                
    def degenUniquness(self):
        if self.getSizeLayer() < 3:
            return False
        
        for i in range(1,len(self.layer)-1):
            
            listUniquness = []
            
            for compareSet in itertools.combinations(range(len(self.layer[i])),2):
                if not self.isUnique(compareSet,i):
                    listUniquness.append(set(compareSet))

            if len(listUniquness) == 0:
                return False
            
#             self.printLayer()
            
#             print "layer: " + str(i) +", unique: " + str(listUniquness) 
            
            numPrevOutput = self.getSizeOutput()
            listNotUniquePC = self.mergeConnectedGraph(listUniquness)
            
#             print "layer: " + str(i) +", NotUni: " + str(listNotUniquePC)
            
            listDeletedPC= []
            for eachNotUnique in listNotUniquePC:
                smallestOne = self.getSmallestOne(eachNotUnique,i)
                eachNotUnique.remove(smallestOne)
                
                self.replaceIndex(i+1, eachNotUnique, smallestOne)
                
                listDeletedPC += eachNotUnique
            
#             print "layer: " + str(i) +", Delete: " + str(listDeletedPC)
            
            listDeletedPC.sort(reverse=True)
            self.adjustIndexByDelete(i+1, listDeletedPC)            
            
            self.deletePerceptrons(i, listDeletedPC)
        
#             self.printLayer()
            self.checkIntegrity(numPrevOutput,"MICRO UNIQUE")
        
        return len(listDeletedPC) > 0
    
    def degenLayer(self):
        if self.getSizeLayer() < 2:
            return False
        
        prevSizeLayer = self.getSizeLayer()
        
        for i in reversed(range(1,self.getSizeLayer())):
            numPrevOutput = self.getSizeOutput()
            setIndex = set()
            for eachPerceptron in self.layer[i]:
                if len(eachPerceptron.indexes) != 1:
                    break
                else:
                    setIndex.add(eachPerceptron.indexes[0])
                    
            if (list(setIndex) == range(len(self.layer[i]))) and (len(self.layer[i]) == len(self.layer[i-1])):
                newLayer = []
                for eachPerceptron in self.layer[i]:                    
                    newLayer.append(self.layer[i-1][eachPerceptron.indexes[0]])                
                
#                 print "Degen Layer------------------------------------------"
#                 self.printLayer()
#                 print "i: ", i, "index set: ", list(setIndex), "range: ", range(len(self.layer[i]))
#                 print "i length: ", len(self.layer[i]), "i-1 length: ", len(self.layer[i-1])
#   
#                 print "\n"
#                 for eachPerceptron in self.layer[i]:
#                     print eachPerceptron
#                 print "\n"
#                 for eachPerceptron in self.layer[i-1]:
#                     print eachPerceptron
#                 
#                 print "\n"
#                 for eachPerceptron in newLayer:
#                     print eachPerceptron
#                 print "\n"                     
                
                self.layer = [self.layer[index] if i-1 != index else newLayer for index in range(self.getSizeLayer())]
                del self.layer[i]
                
#                 self.layer = self.layer[0:i]
#                 self.layer[i-1] = newLayer

#                 self.printLayer()
#                 print "-----------------------------------------------------"
                

                if self.getSizeOutput() != numPrevOutput:
                    self.printLayer()
                    print "i: ", i, "index set: ", list(setIndex), "range: ", range(len(self.layer[i]))
                    print "i length: ", len(self.layer[i]), "i-1 length: ", len(self.layer[i-1])                    

                self.checkIntegrity(numPrevOutput,"Layer Degeneration")

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
#                     print listCliqueN[i], hasLargerClique
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
#             if len(ref) > 0:
            listFirstOneReference.append(ref[0])
#             
#         if len(listFirstOneReference) < 2:
#             return True            
            
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
        temp = Perceptron.PERCEPTRON()
        
        if random.random() < 0.5:
            return temp.calANDgateValue(numInput)
        else:
            return temp.calORgateValue(numInput)
    
    def getRefStructure(self,numOutput):
        if self.checkIndexInLayer(numOutput):
            return []
    
    def getAllReferenced(self,indexInLayer,numTargetLayer=1,numLayer=-1):
        if self.checkIndexInLayer(indexInLayer,numLayer):
            print "Out of Index- Index in layer: ", indexInLayer, "Index of End Layer: ", numLayer, len(self.layer[len(self.layer)-1])
            return []
        
        if self.checkLayer(numTargetLayer):
            print "Out of Layer- Index of Start layer: ", numTargetLayer
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
        
    def getNumLayer(self):
        return len(self.layer)
        
    def getNumTotalPerceptron(self):
        eachNum = [len(self.layer[i]) for i in range(len(self.layer))]
        return sum(eachNum)
    
    def getSizeOutput(self):
        return len(self.layer[len(self.layer)-1])
    
    def randParentByCount(self,parents,indexCount):
        counts = []
        for eachParent in parents:
            counts.append(eachParent.getCount(indexCount))
        
        sel = random.uniform(0,sum(counts)+1)
        
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