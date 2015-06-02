import random

import Logger
import GenePool
import ProblemPool


logger = Logger.LOGGER()
logger.initLogger("Aritifitial Generated","../results/",activate=True)
            
prbPool = ProblemPool.PROBLEM_POOL()
prbPool.initByGenStr(2, 4, 3, logger)

geenpool = GenePool.GENE_POOL()
geenpool.initGenePool(prbPool, 100)

numGeneration = 0
limitGeneration = 500

learningState = True

while learningState:
    if len(geenpool.genePool) < 1:
        print "All dead"
        break
    else:                
        print "\n\tGeneration " + str(numGeneration) + " is started. Pool size: "+ str(len(geenpool.genePool)) + "\n"        
        geenpool.doGame()

        #gp.statLayerCount()
        geenpool.evaluationLR(True)
    #     geenpool.statLayerCount()    
        
    #     numSimulation,numGeneration,nameCategory,strContent,numBlock=-1
        logger.writeGenerationResult(0,numGeneration,"Percent",geenpool.getStrGenerationPercent())
        logger.writeGenerationResult(0,numGeneration,"Diversity",geenpool.getStrDiversity())
        learningState = geenpool.checkLearningState(True)
        
        if limitGeneration == numGeneration:
            print "\nGeneration is over a hundred. It is too long time... The simulation end."                        
            learningState = False
            break            
            
        geenpool.crossover()
        geenpool.mutation()
        geenpool.evolution()
        geenpool.resetCounter()
        geenpool.newGene()
        print "\n\tGeneration " + str(numGeneration) + " is Ended."
        
        numGeneration += 1        

            
print "\n--------------------------------RESULT------------------------------\n"
geenpool.remainBestOne()
print "\Result"
geenpool.resetCounter()
geenpool.excuteBlock(withoutSight = True)
geenpool.calSolvingPercentage()
logger.writeSimulationResult(0, "Result_Percent", geenpool.getStrGenerationPercent())
logger.writeBlockResult(0, "Result_Str", geenpool.getStrStructureBest())
print "\n---------------------------------------------------------------------"
            
            