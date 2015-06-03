import math
import copy
import random

import numpy

import Cell

class GENE_POOL(object):
    def __init__(self):
        pass
    
    def initGenePool(self, prbPool, numPopulation=100):
        self.prbPool = prbPool
        self.genePool = []
        for _ in range(numPopulation):
            newCell = Cell.CELL()
            newCell.initbyPrbpool(prbPool)
            self.genePool.append(newCell)
            
        self.initPopu=numPopulation
        self.probCrossover = 0.7
        self.probMutation = 0.3
        self.probMacroEvolution = 0.1
        self.probMicroEvolution = 0.2
        
        self.numSolvePrb = 0
        self.previousMaxPercentage = -1.0
        self.numGenStaturated = 0
        
        self.strTransfer = "Rectifier"
        self.dictTransfer = {"Rectifier": False,
                             "Step": True}
        
    def doGame(self,blockBank = -1, numBlock = 10, mode=0):
        if blockBank == -1:
            self.excuteBlock(blockBank, mode=mode)
        else:
            for i in range(numBlock):
                if i != blockBank:
                    self.excuteBlock(i, numBlock, mode=mode)
    
    def excuteBlock(self,blockBank = -1, numBlock = 10, mode=0, withoutSight=False ):
        if blockBank == -1:
            blockStart = 0
            blockEnd = self.prbPool.sizeBank
        else:
            blockStart = self.prbPool.sizeBank/numBlock*blockBank
            blockEnd = self.prbPool.sizeBank/numBlock*(blockBank+1)

        for j in range(blockStart, blockEnd):
            self.numSolvePrb += 1.0
            prb = self.prbPool.getOneProblemFromBank(j)
#             if j == blockStart:
#                 print prb, blockStart
#                 print self.prbPool.sizeBank, numBlock, blockBank
            for cell in self.genePool:
                cell.solveProblem(prb, solveWithoutSight=withoutSight, mode=mode)

        return 0
    
    def evaluation(self,enablePrintBest=False):
        newGenePool = []
        bankSize = self.initPopu/(self.prbPool.sizeY+3)
        
        for i in range(-2, self.prbPool.sizeY+1):
            temp = sorted(self.genePool, key=lambda cell: cell.getCount(i), reverse=self.dictTransfer[self.strTransfer])
            newGenePool += copy.deepcopy(temp[0:bankSize])
            #print i, temp[0]
        #print "-1" + str(temp[0])
        
        if enablePrintBest:
            print newGenePool[0]
        self.calSolvingPercentage()
                        
        self.genePool = newGenePool
        
        return len(self.genePool)
    
    def evaluationLR(self,enablePrintBest=False):
        newGenePool = []
        for i in range(-2, self.prbPool.sizeY+1):
            temp = sorted(self.genePool, key=lambda cell: cell.getCount(i), reverse=self.dictTransfer[self.strTransfer])
            newGenePool.append(copy.deepcopy(temp[0]))        
#         print len(newGenePool)
                
        bankSize = self.initPopu/(self.prbPool.sizeY+3)
        if bankSize < 10:
            bankSize = 10
        
        for i in range(-2, self.prbPool.sizeY+1):
            prevSize = 0
            
            listSelected = copy.deepcopy(self.selection(i,bankSize/15,3))
            prevSize += len(listSelected)
            newGenePool += listSelected
            
            listSelected = copy.deepcopy(self.selection(i,bankSize/5,2))
            prevSize += len(listSelected)
            newGenePool += listSelected
            
            listSelected = copy.deepcopy(self.selection(i,bankSize-prevSize,1))
            newGenePool += listSelected
            
            
        if enablePrintBest:
            self.genePool.sort(key=lambda cell: cell.getCount(0), reverse=self.dictTransfer[self.strTransfer])
            print self.genePool[0]

        self.calSolvingPercentage()
        self.genePool = newGenePool
        
        #self.actDigestion()
        
#         print bankSize, len(self.genePool)
        
        return len(self.genePool)
    
    def actDigestion(self):
        popuToHunting = int(math.ceil(len(self.genePool)*0.001/(self.prbPool.sizeY)))
        
        if popuToHunting < 1:
            return False
                
        for eachIndex in range(self.prbPool.sizeY):
            listHunt = self.selection(eachIndex,int(popuToHunting*(1.0-self.classPercentage[0][eachIndex+1])*10.0))
                
            for eachCell in listHunt:
                preyList = self.findAllPreyInRange(eachCell,eachIndex)
                
#                 if len(preyList) > 0:
#                     print "Digest Activate------------------------------------------", eachIndex
                
                for eachPrey in preyList:
                    sizeLayerPrey = eachPrey.getSizeLayer()
                    sizeLayerHunter = eachCell.getSizeLayer()
                    if sizeLayerHunter > sizeLayerPrey:
                        if random.random() < 1.0/(abs(sizeLayerHunter-sizeLayerPrey)**2.2):
#                             print "Eat one"
                            self.genePool.append(self.microevolution([eachCell,eachPrey]))
                    
        return True
                
    def findAllPreyInRange(self,cellHunting,indexOutput):
        listInRange = []
        
        for eachCell in self.genePool:
            if cellHunting.sights[indexOutput].isInSight(eachCell.sights[indexOutput].center):
                listInRange.append(eachCell)
                
        return listInRange        

    def resetCounter(self):
        for cell in self.genePool:
            cell.resetAllCounter()
        self.numSolvePrb = 0

    def evaluationBiosystem(self):
        self.calSolvingPercentage()
        self.adjProbability()
        self.supplyFeedPool()
    
        self.rationFeed()
        
        for cell in self.genePool:
            cell.metabolicAct()
            
        newGenePool = [cell for cell in self.genePool if cell.getFeed() > 0]
        self.genePool = newGenePool
        
        return len(self.genePool)
    
    def checkLearningState(self,isLimited=True,maxLimit=0.95):                
        if isLimited: 
            if self.maxPercentage > maxLimit:            
                return self.checkContinueousSaturated(True,maxLimit)            
        else:
            return self.checkContinueousSaturated(False) 
        
        return True
        
    def checkContinueousSaturated(self,isLimited,maxLimit=0.95):
        if self.previousMaxPercentage == self.maxPercentage:
            self.numGenStaturated += 1
            if self.numGenStaturated < 10:
                if isLimited:
                    print "\nThe best one is over " + str(maxLimit*100)+"% in " + str(self.numGenStaturated) + " time(s)!!!"
                else:
                    print "\nThe best one is saturated in " + str(self.numGenStaturated) + " time(s) with " + str(round(self.maxPercentage*100,2)) + "%!!!"
                return True
            else:
                print "\nThe best is saturated. Learning is over."
                return False                          
        else:
            self.previousMaxPercentage = self.maxPercentage
            self.numGenStaturated = 0
            
        return True
    
    def selectionRandom(self, numToSelection=2, sizeLayer=-1):
        newPool = []
        if sizeLayer == -1:
            newPool = self.genePool
        else:
            for eachCell in self.genePool:
                if eachCell.getSizeLayer() == sizeLayer:
                    newPool.append(eachCell)
                    
        return copy.deepcopy(random.sample(newPool,numToSelection))        
        
    def selection(self, indexOutput=-1, numToSelection=2, sizeLayer=-1):
        if numToSelection == 0:
            return []
        
        newPool = []
        if sizeLayer == -1:
            newPool = self.genePool
        else:
            for eachCell in self.genePool:
                if eachCell.getSizeLayer() == sizeLayer:
                    newPool.append(eachCell)
        
        if len(newPool) == 0:
            return []
                
        newPool.sort(key=lambda cell: cell.getCount(indexOutput), reverse=self.dictTransfer[self.strTransfer])
                
        totalCount = 0.0
        maxCount = 0.0         
        for cell in newPool:
            cellCount = cell.getCount(indexOutput)
            totalCount += cellCount
            if cellCount > maxCount:
                maxCount = cellCount
                
        if not self.dictTransfer[self.strTransfer]:
            totalCount = maxCount*len(newPool) - totalCount
            
        totalCount += len(newPool)
            
        selected = []
        for _ in range(numToSelection):
            selected.append(random.uniform(0,totalCount))
            
        selected.sort()
#         print numToSelection, totalCount, selected
        
        adjustSel = [selected[0]]
        adjustSel += [selected[i+1] - selected[i] for i in range(len(selected)-1)] 
        
#         print "total: ", totalCount
#         print "nor selected: ", selected
#         print "adj selected: ", adjustSel

        selectedCell = []
        indexGenePool = 0
        prevDebt = 0
        for eachSel in adjustSel:
#             print "\tstart: ", eachSel
            eachSel += prevDebt
#             print "\tpre  : ", eachSel

            if eachSel < 1:
#                 print "\tsame : ", eachSel
                selectedCell.append(copy.deepcopy(newPool[indexGenePool-1]))
                prevDebt = eachSel
                continue
            else:                
                for indexNow, eachCell in enumerate(newPool[indexGenePool:]):
                    eachCount = eachCell.getCount(indexOutput)
                    if not self.dictTransfer[self.strTransfer]:
                        eachCount = maxCount - eachCount
                    
                    eachSel -= eachCount + 1.0
#                     print "\tproc : ", eachSel
                    if eachSel < 1:
                        selectedCell.append(copy.deepcopy(eachCell))
                        indexGenePool = indexNow+1
                        prevDebt = eachSel
                        break
        
#         print "\t\tTotal: ", len(selectedCell)
#         print "selected cell: ", selectedCell

#         i = 0
#         j = 0
#                 
#         while i < numToSelection:
#             cell = self.genePool[j]
#             cnt = cell.getCount(indexOutput)
#             if cnt > adjustSel[i]:
#                 selectedCell.append(cell)
#                 i += 1
#             else:
#                 adjustSel[i] -= cnt
#             
#             j += 1
#             if j == len(self.genePool):
#                 selectedCell.append(cell)
#                 break

        return selectedCell[0:numToSelection]
    
    def selectionByFeed(self, indexOutput=-1, numToSelection=2):
        
        totalFeed = self.getFeed(indexOutput) + len(self.genePool)
        selected = []        
                
        print totalFeed
        for _ in range(numToSelection):
            selected.append(random.randint(0,totalFeed))
            
        selected = sorted(selected)
        
        adjustSel = [selected[0]]
        
        for i in range(1,len(selected)):
            adjustSel.append(selected[i]-selected[i-1]) 
                
        selectedCell = []
        i = 0 
        for cell in self.genePool:
            adjustSel[i] -= (cell.getFeed(indexOutput)+1)
            if adjustSel[i] < 0:
                selectedCell.append(cell)
                i += 1
                if i < numToSelection:
                    adjustSel[i] += adjustSel[i-1]
                else:
                    break
        
        return selectedCell
        
    def crossover(self):
        prePopu = len(self.genePool)
        
        populationCrossover = int(len(self.genePool)*0.1)
                
        for i in range(-1,self.prbPool.sizeY):
            for _ in range(populationCrossover):
                if random.random() < self.probCrossover:
                    parents = self.selection(i)
                    self.genePool.append(self.rnaCrossover(parents))
                    
#                 elif random.random() < self.probMicroEvolution/2:
#                     parents = self.selection(i)
#                     self.microevolution(parents)

        return len(self.genePool)-prePopu
    
    def mutation(self):
        prePopu = len(self.genePool)
        for eachCell in self.genePool:
                       
            if random.random() < self.probMutation:
                newCell = copy.deepcopy(eachCell)
#                 if len(newCell.layer[0][0].indexes) <= 1:
#                     print "src"
#                     print id(eachCell)
#                     print eachCell                
#                     print "aftercopy"
#                     print id(newCell)
#                     print newCell
#                     
                newCell.mutate(self.prbPool.sizeX)
                self.genePool.append(newCell)
        
        return len(self.genePool)-prePopu
                
    def evolution(self):
        prePopu = len(self.genePool)
        populationEvolution = int(len(self.genePool)*0.03)
        
        for i in range(-1,self.prbPool.sizeY):
            for _ in range(populationEvolution):
                if random.random() < self.probMacroEvolution:
                    parents = self.selection(i)                    
                    self.genePool.append(self.macroevolution(parents))

                elif random.random() < self.probMicroEvolution:
                    parents = self.selection(i)
                    if parents[0].getSizeLayer() != 1 or parents[1].getSizeLayer() != 1:                    
                        self.genePool.append(self.microevolution(parents))
                        
        return len(self.genePool)-prePopu
                               
    def newGene(self):
        prePopu = len(self.genePool)
#         populationNewGene = int(1.0-self.maxPercentage)*len(self.genePool)
        populationNewGene = int(1.0*len(self.classPercentage[0])-sum(self.classPercentage[0]))*len(self.genePool)
        for _ in range(populationNewGene):
            newCell = Cell.CELL()
            newCell.initbyPrbpool(self.prbPool)
            self.genePool.append(newCell)
            
        return len(self.genePool)-prePopu
                                           
    def rnaCrossover(self, parents):
        newCell = Cell.CELL()        
        newCell.initbyRnas(parents)
        
        return newCell
            
    def microevolution(self, parents):
        newCell = Cell.CELL()
        newCell.initbyMicevol(parents)
        
        return newCell
    
    def macroevolution(self,parents):
        newCell = Cell.CELL()
        newCell.initbyMacevol(parents)
                
        return newCell        
    
    def calSolvingPercentage(self):
        #if evaluation value is larger is better
        classPercentage = [[] for _ in range(self.prbPool.sizeY+1)]
        
#         print self.numSolvePrb, self.genePool[0].getCount(1)
                
        if self.dictTransfer[self.strTransfer]:
            for i in range(self.prbPool.sizeY+1):
                for cell in self.genePool:
                    classPercentage[i].append(float(cell.getCount(i)/float(self.numSolvePrb)))                    
                        
        #value is close to 0 is better
        else:
            for i in range(self.prbPool.sizeY+1):
                for cell in self.genePool:
                    classPercentage[i].append((float(self.numSolvePrb) - float(cell.getCount(i)))/float(self.numSolvePrb))
                    
                    
        self.classPercentage = [[max(classPercentage[i]) for i in range(self.prbPool.sizeY+1)],
                                [numpy.mean(classPercentage[i]) for i in range(self.prbPool.sizeY+1)]]
#         print self.classPercentage
        self.maxPercentage = self.classPercentage[0][0]
        self.avgPercentage = self.classPercentage[1][0]

#         print self.classPercentage
        #print self.prbPool.sizeBank
        print '\t {0:15} {1:3.5f} {2:3.5f}'.format("Total", round(self.classPercentage[0][0],5), round(self.classPercentage[1][0],5))
        for i in range(1,self.prbPool.sizeY+1):
            print '\t {0:15} {1:3.5f} {2:3.5f}'.format(self.prbPool.nameY[i-1], round(self.classPercentage[0][i],5), round(self.classPercentage[1][i],5))
        
    def adjProbability(self):
        pass
    
    def supplyFeedPool(self):
        self.feedPool = float(self.prbPool.sizeBank*len(self.genePool))*(1.0+self.avgPercentage)
        
    def rationFeed(self):
        for eachCell in self.genePool:
            for i in range(self.prbPool.sizeY):
                prob = float(eachCell.getCount(i))/float(self.prbPool.sizeBank)
                feed = self.calGiveFeedAmount(eachCell,prob)
                if self.feedPool > 0:
                    eachCell.gainFeed(i, feed)
                    self.feedPool -= feed

    def calGiveFeedAmount(self,singelCell,multiplier=1):
        return int(float(singelCell.getCellSize())*(1.0+multiplier))        
        
    def getFeed(self, indexOutput = -1):
        totalFeed = 0
        for cell in self.genePool:
            totalFeed += cell.getFeed(indexOutput)
        
        return totalFeed
            
    def checkZeroLayer(self):
        for eachCell in self.genePool:
            if len(eachCell.layer[0][0].indexes) <= 1:
                print id(eachCell)
                print eachCell    
                
    def statLayerCount(self):
        
        stats = [0 for _ in range(3)]
        
        for eachCell in self.genePool:
            stats[eachCell.getSizeLayer()-1] += 1
            
        for i, eachStat in enumerate(stats):            
            print i, eachStat
            
# #         stats = sorted(self.genePool, key=lambda cell: cell.getCountRight(), reverse=True)
#         for i, eachLayerPool in enumerate(stats):
#             eachLayerPool.sort(key=lambda statArray: sum(statArray), reverse=True)            
#             
#             for j, elements in enumerate(eachLayerPool):
#                 if j == 0:
#                     print elements
#                 
#                 if j > 4:
#                     break
#                 
#                 print i, j, sum(elements), elements
                
    def remainBestOne(self):
        temp = sorted(self.genePool, key=lambda cell: cell.getCount(0), reverse=self.dictTransfer[self.strTransfer])
        self.genePool = [temp[0]]
        return copy.deepcopy(temp[0])
            
    def getStrGenerationPercent(self):    
        strPercent = str(self.maxPercentage) +","+ str(self.avgPercentage) +","
        for i in range(self.prbPool.sizeY):
            strPercent += str(self.classPercentage[0][i]) +","+ str(self.classPercentage[1][i]) +","
                        
        return strPercent
    
    def getStrDiversity(self):        
        maxNumLayer = self.findMaxNumLayer()
        maxNumPerceptron = self.findMaxNumPerceptron()
        
        statCells = [[0 for _ in range(maxNumPerceptron)] for _ in range(maxNumLayer)]
        for eachCell in self.genePool:
            statCells[eachCell.getNumLayer()-1][eachCell.getNumTotalPerceptron()-1] += 1
        
        strDiversity = ""
        for i in range(maxNumLayer):
            for j in range(maxNumPerceptron):
                if statCells[i][j] > 0:
                    strDiversity += str(i+1)+"_"+str(j+1) +","+ str(statCells[i][j]) + ","
                    
        return strDiversity
    
    def findMaxNumLayer(self):
        maxNumLayer = 0
        
        for eachCell in self.genePool:
            nowNumLayer = eachCell.getNumLayer()
            if nowNumLayer > maxNumLayer:
                maxNumLayer = nowNumLayer
                
        return maxNumLayer
    
    def findMaxNumPerceptron(self):
        maxNumPerceptron = 0
        
        for eachCell in self.genePool:
            nowNumPerceptron = eachCell.getNumTotalPerceptron()
            if nowNumPerceptron > maxNumPerceptron:
                maxNumPerceptron = nowNumPerceptron
                
        return maxNumPerceptron
    
    def getStrStructureBest(self):
        cellBest = self.genePool[0]
        
        return cellBest.getStrStructure()

    
    
# prbPool = ProblemPool.PROBLEM_POOL("./balance.csv")
# gp = GENE_POOL()
# gp.initGenePool(prbPool, 100)
# print len(gp.genePool)
# print gp.doGame()
# print gp.evaluation() 
#    
# selected = gp.selection()
# for cell in selected:
#     print cell
#    
# print "rnaCrossOver"
# testCell = gp.rnaCrossover(selected) 
# print testCell
# 
# print "macroEvolution"
# testCell = gp.macroevolution(selected) 
# print testCell

# 
# print "Mutate"
# testCell.mutate(prbPool.sizeX)
# print testCell


    