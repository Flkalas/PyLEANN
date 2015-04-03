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
        
        self.previousMaxPercentage = 0 
        
    def doGame(self):
        
#         prbTime = []
        for i in range(self.prbPool.sizeBank):            
            prb = self.prbPool.getOneProblemFromBank(i)
            for cell in self.genePool:
#                 arrTime = [time.time()]
                cell.solveProblem(prb)
#                 arrTime.append(time.time())        
#                 prbTime.append(arrTime[1]-arrTime[0])
#         print numpy.mean(prbTime)
        
        return 0
    
    def evaluation(self,enablePrintBest=False):        
        newGenePool = []
        bankSize = self.initPopu/(self.prbPool.sizeY+1)
        
        for i in range(-1, self.prbPool.sizeY):
            temp = sorted(self.genePool, key=lambda cell: cell.getCount(i), reverse=True)
            newGenePool += copy.deepcopy(temp[0:bankSize])
            print i, temp[0]
                    
        temp = sorted(self.genePool, key=lambda cell: cell.getCountRight(), reverse=True)
        newGenePool += copy.deepcopy(temp[0:bankSize])
        print "-1" + str(temp[0])
        
        if enablePrintBest:
            print newGenePool[0]        
        self.calSolvingPercentage()
                        
        self.genePool = newGenePool
        
        return len(self.genePool)

    def resetCounter(self):
        for cell in self.genePool:
            cell.resetAllCounter()

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
    
    def checkLearningState(self):                
        if self.maxPercentage > 0.95:            
            if self.previousMaxPercentage == self.maxPercentage:
                self.numGenStaturated += 1
                if self.numGenStaturated < 10:
                    print "The best one is over 95.00% in " + str(self.numGenStaturated) + "time(s)!!!"
                    return True
                else:
                    print "The best is saturated. Learning is over."
                    return False                          
            else:
                self.previousMaxPercentage = self.maxPercentage
        
        self.numGenStaturated = 0
        
        return True
    
    def selection(self, indexOutput=-1, numToSelection=2):
        
        totalCount = 0
        
        for cell in self.genePool:
            totalCount += cell.getCount(indexOutput)
            
        selected = []

        for _ in range(numToSelection):
            selected.append(random.randint(0,totalCount))
            
        selected = sorted(selected)
        
        adjustSel = [selected[0]]
        
        for i in range(1,len(selected)):
            adjustSel.append(selected[i]-selected[i-1]) 

        selectedCell = []
        i = 0
        j = 0
                
        while i < numToSelection:
            cell = self.genePool[j]
            cnt = cell.getCount(indexOutput)
            if cnt > adjustSel[i]:
                selectedCell.append(cell)
                i += 1
            else:
                adjustSel[i] -= cnt
            
            j += 1
            if j == len(self.genePool):
                selectedCell.append(cell)
                break

        return selectedCell[0:2]
    
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
                    if parents[0].getSizeLayer() == parents[1].getSizeLayer():
                        self.genePool.append(self.macroevolution(parents))

                elif random.random() < self.probMicroEvolution:
                    parents = self.selection(i)
                    if parents[0].getSizeLayer() != 1 or parents[1].getSizeLayer() != 1:                    
                        self.genePool.append(self.microevolution(parents))
                        
        return len(self.genePool)-prePopu
                               
    def newGene(self):
        prePopu = len(self.genePool)
        populationNewGene = int(len(self.genePool)*0.05)        
        for _ in range(populationNewGene):
            newCell = Cell.CELL()
            newCell.initbyPrbpool(self.prbPool)
            self.genePool.append(newCell)
            
        return len(self.genePool)-prePopu
                                           
    def rnaCrossover(self, parents):
        newCell = Cell.CELL()        
        newCell.initbyRnas(parents, self.prbPool)
        
        return newCell
            
    def microevolution(self, parents):
        newCell = Cell.CELL()
        newCell.initbyMicevol(parents, self.prbPool)
        
        return newCell
    
    def macroevolution(self,parents):
        newCell = Cell.CELL()
        newCell.initbyMacevol(parents, self.prbPool)
                
        return newCell        
    
    def calSolvingPercentage(self):
        percentage = []
        for cell in self.genePool:
                percentage.append(float(cell.getCountRight())/float(self.prbPool.sizeBank))
            
        classPercentage = [[] for _ in range(self.prbPool.sizeY)]
        for i in range(self.prbPool.sizeY):
            for cell in self.genePool:
                classPercentage[i].append(float(cell.getCount(i)/float(self.prbPool.sizeBank)))
                
        self.maxPercentage = max(percentage)
        self.avgPercentage = numpy.mean(percentage)

        print self.prbPool.sizeBank
        print '\t {0:15} {1:3.5f} {2:3.5f}'.format("Total", round(max(percentage),5), round(numpy.mean(percentage),5))
        for i in range(self.prbPool.sizeY):            
            print '\t {0:15} {1:3.5f} {2:3.5f}'.format(self.prbPool.nameY[i], round(max(classPercentage[i]),5), round(numpy.mean(classPercentage[i]),5))
            
                     
        
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
        
        stats = [[] for _ in range(10)]
        
        for eachCell in self.genePool:
            stats[eachCell.getSizeLayer()].append(eachCell.getArrayClassCount())
            
#         stats = sorted(self.genePool, key=lambda cell: cell.getCountRight(), reverse=True)
        for i, eachLayerPool in enumerate(stats):
            eachLayerPool.sort(key=lambda statArray: sum(statArray), reverse=True)            
            
            for j, elements in enumerate(eachLayerPool):
                if j == 0:
                    print elements
                
                if j > 4:
                    break
                
                print i, j, sum(elements), elements
            
        

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


    