import GenePool
import ProblemPool

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
    
            gp.doGame()
    
            #gp.statLayerCount()
            gp.evaluation(False)
            learningState = gp.checkLearningState()
            
            gp.crossover()
            gp.mutation()
            gp.evolution()
            gp.resetCounter()        
            gp.newGene()
            
            print "\n\tGeneration " + str(generation) + " is Ended."
            
            generation += 1
            
            if generation > 100:
                print "\nGeneration is over a hundred. It is too long time... The simulation end."
                learningState = False

numTimes = 0
while numTimes < 100:
    learningLeann("./iris.csv")
    numTimes += 1
    print "\n" + str(numTimes) + " Simulation is ended."
