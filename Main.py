import GenePool
import ProblemPool

prbPool = ProblemPool.PROBLEM_POOL("./iris.csv")  
gp = GenePool.GENE_POOL()
gp.initGenePool(prbPool, 400)
generation = 0
learningState = True

while learningState:
    if len(gp.genePool) < 1:
        print "All dead"
        break
    else:
        print "\n" + str(generation) + " Pool size: "+ str(len(gp.genePool)) + "\n"

        gp.doGame()

        gp.statLayerCount()
        gp.evaluation(True)
        learningState = gp.checkLearningState()
        
        gp.crossover()
        gp.mutation()
        gp.evolution()
        gp.resetCounter()        
        gp.newGene()
        
        generation += 1
        
        if generation > 100:
            print "Generation is over a hundred. It is too long time... The simulation end."
            learningState = False


