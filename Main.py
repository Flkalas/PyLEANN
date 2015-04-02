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
#         arrTime = [time.time()]
        gp.doGame()
#         arrTime.append(time.time())
        gp.statLayerCount()
        gp.evaluation(True)
        learningState = gp.checkLearningState()
        
#         arrTime.append(time.time())
        gp.crossover()
#         arrTime.append(time.time())
        gp.mutation()
#         arrTime.append(time.time())
        gp.evolution()
#         arrTime.append(time.time())
        gp.resetCounter()
        
        gp.newGene()
         
        generation += 1
#         for i in range(len(arrTime)-1):
#             print i, arrTime[i+1] - arrTime[i]

