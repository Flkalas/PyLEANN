import GenePool
import ProblemPool

def operateGenepool(geenpool, blockBank = -1, numBlock = 10):
    geenpool.doGame(blockBank,numBlock)

    #gp.statLayerCount()
    geenpool.evaluation(False)
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

def learningLeannCrossValidation(nameFile, numBlock = 10):
    for i in range(numBlock):        
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
                learningState = operateGenepool(gp,i,numBlock)                
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
        print "\n-------------------------------------------------------------------------------"
                
numTimes = 0
while numTimes < 100:
    learningLeannCrossValidation("./iris.csv")
    numTimes += 1
    print "\n" + str(numTimes) + " Simulation is ended."
