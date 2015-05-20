import os
import sys

import Logger
import GenePool
import ProblemPool

limitGeneration = 500

def operateGenepool(geenpool, logger="", numSimulation=0, numGeneration=0,  blockBank = -1, numBlock = 10):
    geenpool.doGame(blockBank,numBlock)

    #gp.statLayerCount()
    geenpool.evaluationLR(True)
    geenpool.statLayerCount()
    
    
#     numSimulation,numGeneration,nameCategory,strContent,numBlock=-1
    logger.writeGenerationResult(numSimulation,numGeneration,"Percent",geenpool.getStrGenerationPercent(),blockBank)
    logger.writeGenerationResult(numSimulation,numGeneration,"Diversity",geenpool.getStrDiversity(),blockBank)
    learningState = geenpool.checkLearningState(True)
    
    if limitGeneration == numGeneration:
        return False
        
    geenpool.crossover()
    geenpool.mutation()
    geenpool.evolution()
    geenpool.resetCounter()
    geenpool.newGene()
    
    return learningState

def learningLeann(nameFile):
    prbPool = ProblemPool.PROBLEM_POOL(nameFile)
    gp = GenePool.GENE_POOL()
    gp.initGenePool(prbPool, 100)
    generation = 0
    learningState = True
    
    while learningState:
        if len(gp.genePool) < 1:
            print "All dead"
            break
        else:
            print "\n\tGeneration " + str(generation) + " is started. Pool size: "+ str(len(gp.genePool)) + "\n"
    
            learningState = operateGenepool(gp)
            
            print "\n\tGeneration " + str(generation) + " is Ended."
            
            generation += 1
            
            if generation > 100:
                print "\nGeneration is over a hundred. It is too long time... The simulation end."
                learningState = False


def excuteSingleBlockCrossValidation(indexBlock, logger, nameFile, numSimulation=0, numBlock=10):
    prbPool = ProblemPool.PROBLEM_POOL()
    prbPool.initFromFile(nameFile,True,numBlock)
            
    gp = GenePool.GENE_POOL()
    gp.initGenePool(prbPool, 100)
    generation = 0
    learningState = True
    
    while learningState:
        if len(gp.genePool) < 1:
            print "All dead"
            break
        else:                
            print "\n\tGeneration " + str(generation) + " is started. Pool size: "+ str(len(gp.genePool)) + "\n"        
            learningState = operateGenepool(gp,logger,numSimulation,generation,indexBlock,numBlock)                
            print "\n\tGeneration " + str(generation) + " is Ended."
            
            generation += 1
            if generation > limitGeneration:
                print "\nGeneration is over a hundred. It is too long time... The simulation end."
                learningState = False
                
    print "\n--------------------------------TEST SET " + str(indexBlock) + " RESULT------------------------------\n"
    gp.remainBestOne()
    print "\tTrain set result"
    gp.resetCounter()
    gp.doGame(indexBlock,numBlock)
    gp.calSolvingPercentage()
    logger.writeSimulationResult(numSimulation, "Train_Percent", gp.getStrGenerationPercent(), indexBlock)    
    print ""
    print "\tTest set result"        
    gp.resetCounter()
    gp.excuteBlock(indexBlock, numBlock, True)
    gp.calSolvingPercentage()
    logger.writeSimulationResult(numSimulation, "Test_Percent", gp.getStrGenerationPercent(), indexBlock)
    
    logger.writeBlockResult(numSimulation, "Train_Best", gp.getStrStructureBest(), indexBlock)
    print "\n-------------------------------------------------------------------------------"
        
def learningLeannCrossValidation(logger, nameFile, numSimulation=0, numBlock=10):
    for i in range(numBlock):
        excuteSingleBlockCrossValidation(i, logger, nameFile, numSimulation, numBlock)


nameFile = "./iris.csv"
shellExecuteBlock = -1
print sys.argv, len(sys.argv) 
if len(sys.argv) > 1:
    nameFile = sys.argv[1]
    if not os.path.isfile(nameFile):
        print "There is no test set named as ", nameFile
        nameFile = "./iris.csv"
        
    if len(sys.argv) == 3:
        shellExecuteBlock = int(sys.argv[2])        
        if shellExecuteBlock > 9:
            print "Execute block number out of range", shellExecuteBlock
            shellExecuteBlock = -1            
print nameFile, shellExecuteBlock

antLogger = Logger.LOGGER()
antLogger.initLogger(nameFile,"../results/",activate=True)

if shellExecuteBlock == -1:
    numTimes = 0
    while numTimes < 10:
        learningLeannCrossValidation(antLogger, nameFile, numSimulation=numTimes)
        numTimes += 1
        print "\n" + str(numTimes) + " Simulation is ended."
else:
    excuteSingleBlockCrossValidation(shellExecuteBlock, antLogger, nameFile, numSimulation=0, numBlock=10)