import copy
import itertools

class QM(object):
    def __init__(self):
        pass
        
    def simplify(self, ones):        
        self.sizeBit = self.calSizeBits(ones)
        
        originalDecodedOnes = self.decodeOnes(ones)
        onesToProcess = copy.deepcopy(originalDecodedOnes)
        
        print self.sizeBit, len(originalDecodedOnes)
        
        #Phase 1
        listResult = []
        isNotEnd = True
        while(isNotEnd):
            listCompress = self.compressOnes(onesToProcess)
            listResult += listCompress[1]
            onesToProcess = listCompress[0]
            
            if len(listCompress[0]) == 0:
                isNotEnd = False
        
        #Phase 2
        resultEnableBlocks = self.selectBlocks(originalDecodedOnes,listResult)
        if len(resultEnableBlocks) > 2:
            print resultEnableBlocks
            while(True):
                pass
        
        return resultEnableBlocks[0]
        
    def decodeOnes(self, ones):        
        formatStr = '{:0' + str(self.sizeBit) + 'b}'
        
        decodedOnes = []        
        for eachOnes in ones:            
            binaryNumber = formatStr.format(eachOnes)
            decodedOnes.append(binaryNumber)
            
        return decodedOnes
    
    def calSizeBits(self,ones):
        maxNumber = max(ones)
        binaryMaxNumber = bin(maxNumber)[2:]
        sizeBits = len(binaryMaxNumber)
        
        return sizeBits
        
    def compressOnes(self,decodedOnes):
        isCompressd = [False for _ in range(len(decodedOnes))]
        setCompressd = set()
        for eachSet in itertools.combinations(range(len(decodedOnes)),2):            
            listCombo = list(eachSet)
            comboOnes = [decodedOnes[indexOnes] for indexOnes in listCombo]            
            
            resultCombine = self.tryToCombine(comboOnes)
            if resultCombine:
                for eachIndex in listCombo:
                    isCompressd[eachIndex] = True
            
                setCompressd.add(resultCombine)
                
        listUncompressed = []
        for i, eachJudgeOnes in enumerate(isCompressd):
            if not eachJudgeOnes:
                listUncompressed.append(decodedOnes[i])
               
        listCompressed = list(setCompressd)
        
        return [listCompressed, listUncompressed]

    def tryToCombine(self,comboOnes):
        countDiff = 0
        indexDiff = -1
        for strIndex in range(self.sizeBit):        
            if comboOnes[0][strIndex] != comboOnes[1][strIndex]:
                countDiff += 1
                indexDiff = strIndex

        if countDiff == 1:            
            listCombined = list(comboOnes[0])            
            listCombined[indexDiff] = '-'
            strCombined = "".join(listCombined)
            
            return strCombined
        else:
            return False
        
    def selectBlocks(self,rawOnes,compressedOnes):    
        enableCombination = []
        setRawOnes = set(rawOnes)
        
        for sizeCombination in range(len(compressedOnes)+1):            
            for eachCombination in itertools.combinations(compressedOnes,sizeCombination):
                setResultCombination = set()
                listCombination = list(eachCombination)
                
                for eachCompressedOne in listCombination:
                    
                    listDepressedOnes = self.getAllOnes(eachCompressedOne)                    
                    setDepressedOnes = set(listDepressedOnes)
                    #print listDepressedOnes, setDepressedOnes
                    
                    setResultCombination = setResultCombination.union(setDepressedOnes)
                    #print setResultCombination
                    
                if setResultCombination == setRawOnes:
                    enableCombination.append(listCombination)
        
        return enableCombination
        
    def getAllOnes(self,compressedOne):        
        listDepressedOnes = []
        
        baseInput = list(compressedOne)
        for i, eachIndex in enumerate(baseInput):
            if eachIndex == '-':
                baseInput[i] = '0'
            
        indexCompressed = []        
        for i in range(len(compressedOne)):
            if compressedOne[i] == '-':
                indexCompressed.append(i)
                
        for sizeCombination in range(len(indexCompressed)+1):
            for indexSet in itertools.combinations(indexCompressed,sizeCombination):                
                combinedInput = copy.deepcopy(baseInput)
                listSubset = list(indexSet)
                for eachInput in listSubset:
                    combinedInput[eachInput] = '1'                    
                listDepressedOnes.append("".join(combinedInput))
        
        return listDepressedOnes
    
        