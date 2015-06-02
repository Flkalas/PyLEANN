import Logger
import GenePool
import ProblemPool

def singleRandomStructureTest(numInput, numOutput, numLayer, logger, numSimulation):                
    prbPool = ProblemPool.PROBLEM_POOL()
    prbPool.initByGenStr(numInput, numOutput, numLayer, logger, numSimulation)
    
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
            geenpool.doGame(mode=2)
    
            #gp.statLayerCount()
            geenpool.evaluationLR(True)
        #     geenpool.statLayerCount()    
            
        #     numSimulation,numGeneration,nameCategory,strContent,numBlock=-1
            logger.writeGenerationResult(numSimulation,numGeneration,"Percent",geenpool.getStrGenerationPercent())
            logger.writeGenerationResult(numSimulation,numGeneration,"Diversity",geenpool.getStrDiversity())
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
    geenpool.resetCounter()
    geenpool.excuteBlock(withoutSight = True, mode=2)
    geenpool.calSolvingPercentage()
    logger.writeSimulationResult(numSimulation, "Result_Percent", geenpool.getStrGenerationPercent())
    logger.writeBlockResult(numSimulation, "Result_Str", geenpool.getStrStructureBest())
    print "\n---------------------------------------------------------------------"

simulLogger = Logger.LOGGER()
simulLogger.initLogger("Aritifitial Generated","../results/",activate=True)

numSimulation = 0

for iterInput in range(2,13):
    for iterOutput in range(2,6):
        for iterLayer in range(1,3):
            singleRandomStructureTest(iterInput,iterOutput,iterLayer,simulLogger, numSimulation)
            numSimulation += 1
            



        