class RNA_ELEMENT(object):
    def __init__(self):
        pass
    
    def __str__(self):        
        return str(self.indexInLayer) + " " + str(self.reference)
    
    def initRNA(self,pc,indexInLayer):
        self.indexInLayer = indexInLayer
        self.reference = []
        
        for ref in pc.indexes:
            self.reference.append(ref) 
        