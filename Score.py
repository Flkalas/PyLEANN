import math

class CONTINGENCY_TABLE(object):    
    def __init__(self):
        self.table = [[0.0 for _ in range(2)] for _ in range(2)]
        self.updateNames()
                
    def getTPR(self):
        self.updateNames()
        return self.TP/self.P
    
    def getSPC(self):
        self.updateNames()
        return self.TN/self.N
        
    def getPPV(self):
        self.updateNames()
        return self.TP/(self.TP + self.FP)
        
    def getNPV(self):
        self.updateNames()
        return self.TN/(self.TN + self.FN)
        
    def getFPR(self):
        self.updateNames()
        return self.FP/self.N
        
    def getFDR(self):
        self.updateNames()
        return self.FP/(self.TP + self.FP)
        
    def getACC(self):
        self.updateNames()
        return (self.TP+self.TN)/(self.P+self.N)
    
    def getF1(self):
        self.updateNames()
        return  2*self.TP/(2*self.TP+self.FP+self.FN)
    
    def getMCC(self):
        self.updateNames()
        return (self.TP*self.TN - self.FP*self.FN)/math.sqrt((self.TP+self.FP)*(self.TP+self.FN)*(self.TN+self.FP)*(self.TN+self.FN))
        
    def getInformedeness(self):        
        return self.getTPR()+self.getSPC()
        
    def getMarkedness(self):        
        return self.getPPV()+self.getNPV()
    
    def getLR_Plus(self):
        return self.getTPR()/self.getFPR()
    
    def getLR_Minus(self):
        return self.getFNR()/self.getTNR()
    
    def getDOR(self):
        return self.getLR_Plus()/self.getLR_Minus()
        
        
    def resetTable(self):
        self.table = [[0 for _ in range(2)] for _ in range(2)]
        
    def updateNames(self):
        self.TP = self.table[0][0] 
        self.FP = self.table[0][1] 
        self.FN = self.table[1][0] 
        self.TN = self.table[1][1]
        self.P = self.TP + self.FN
        self.N = self.FP + self.TN    

class SCORE(object):
    def __init__(self, prbPool):
        self.CtClass = [CONTINGENCY_TABLE() for _ in range(prbPool.sizeY)]
        self.CtInSight = [CONTINGENCY_TABLE() for _ in range(prbPool.sizeY)]
        
    
    