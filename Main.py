import os
import sys

import Logger
import GenePool
import ProblemPool

def operateGenepool(geenpool, logger="", numSimulation=0, numGeneration=0,  blockBank = -1, numBlock = 10):
    geenpool.doGame(blockBank,numBlock)

    #gp.statLayerCount()
    geenpool.evaluation(False)
#     numSimulation,numGeneration,nameCategory,strContent,numBlock=-1
    logger.writeGenerationResult(numSimulation,numGeneration,"Percent",geenpool.getStrGenerationPercent(),blockBank)
    logger.writeGenerationResult(numSimulation,numGeneration,"Diversity",geenpool.getStrDiversity(),blockBank)
    learningState = geenpool.checkLearningState(True)
    
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

def learningLeannCrossValidation(nameFile, numSimulation=0, numBlock=10):
    antLogger = Logger.LOGGER()
    antLogger.initLogger(activate=True)    
    
    for i in range(numBlock):
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
                learningState = operateGenepool(gp,antLogger,numSimulation,generation,i,numBlock)                
                print "\n\tGeneration " + str(generation) + " is Ended."
                
                generation += 1                
                if generation > 100:
                    print "\nGeneration is over a hundred. It is too long time... The simulation end."
                    learningState = False
                    
        print "\n--------------------------------TEST SET " + str(i) + " RESULT------------------------------\n"
        gp.remainBestOne()
        gp.resetCounter()        
        gp.excuteBlock(i, numBlock)
        gp.evaluation(False)
        antLogger.writeBlockResult(numSimulation, "Train_Best", gp.getStrStructureBest(), i)
        antLogger.writeSimulationResult(numSimulation, "Test_Percent", gp.getStrGenerationPercent(), i)
        print "\n-------------------------------------------------------------------------------"

nameFile = "./iris.csv"
if len(sys.argv) > 1:
    nameFile = sys.argv[1]
    if not os.path.isfile(nameFile):
        nameFile = "./iris.csv"
print sys.argv
        
numTimes = 0
while numTimes < 100:
    learningLeannCrossValidation(nameFile, numSimulation=numTimes)
    numTimes += 1
    print "\n" + str(numTimes) + " Simulation is ended."

    