import os
import numpy

#find all prefix number
i = 0
listPrefix = []
while len(listPrefix) < 5:
    if os.path.isfile("_"+ str(i) + ".txt"):
        listPrefix.append(i)
    
    i += 1

print listPrefix

numRangeInput = 5
numRangeOutput = 5
numRangeLayer = 3

sumIndex = 0

dataSet = []

for iterInput in range(numRangeInput):
    
    dataInputSet = []
    
    for iterOutput in range(numRangeOutput):
        
        dataOutputSet = []
        
        for iterLayer in range(numRangeLayer):
            
            dataLayerSet = [[],[]]
                        
            for eachPrefix in listPrefix:                                
                nameFile = "_"+ str(eachPrefix) + "_"+ str(sumIndex)
                
                nameFilePercent = nameFile + "_Percent.csv"
                nameFileGenerated = nameFile + "_Generated_Str.csv"
                nameFileResulted = nameFile + "_Result_Str.csv"

                numPercent = 0.0
                numGeneratedPerceptron = 0
                numResultedPerceptron = 0

                if os.path.isfile(nameFilePercent):
                    fileOpened = open(nameFilePercent,'r')
                    newList = fileOpened.readlines()
                    fileOpened.close()
                    
                    listPercent = newList[-1].split(',')
                    numPercent = float(listPercent[1])
                                        
#                     print sumIndex, iterInput, iterOutput, iterLayer, eachPrefix, float(listPercent[1])
                    
                if os.path.isfile(nameFileGenerated):
                    fileOpened = open(nameFileGenerated,'r')
                    newList = fileOpened.readlines()
                    fileOpened.close()
                                        
                    for eachLine in newList:
                        if eachLine.find("Perceptron") != -1:
                            numGeneratedPerceptron += 1
                            
#                     print sumIndex, iterInput, iterOutput, iterLayer, eachPrefix, numGeneratedPerceptron
                    
                if os.path.isfile(nameFileResulted):
                    fileOpened = open(nameFileResulted,'r')
                    newList = fileOpened.readlines()
                    fileOpened.close()
                                        
                    for eachLine in newList:
                        if eachLine.find("Perceptron") != -1:
                            numResultedPerceptron += 1                
                    
#                     print sumIndex, iterInput, iterOutput, iterLayer, eachPrefix, numResultedPerceptron
                    
                if numGeneratedPerceptron > 0 and numResultedPerceptron > 0 and numPercent != 0.0:                    
                    dataLayerSet[0].append(numPercent)
                    dataLayerSet[1].append(float(numResultedPerceptron)/float(numGeneratedPerceptron))
            
            sumIndex += 1
            
#             newDataLayerSet = []
#             for eachData in dataLayerSet:
#                 meanData = numpy.mean(eachData)              
#                 stddevData = numpy.std(eachData)
#                 
#                 newDataLayerSet.append([meanData,stddevData])
            
            
#             dataOutputSet.append(newDataLayerSet)
            dataOutputSet.append(dataLayerSet)
        dataInputSet.append(dataOutputSet)
    dataSet.append(dataInputSet)

print dataSet

for iterInput in range(numRangeInput):
    dataInput = [[],[]]
    for iterOutput in range(numRangeOutput):
        for iterLayer in range(numRangeLayer):
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                dataInput[i] += eachData
    
    print iterInput+2, numpy.mean(dataInput[0]), numpy.std(dataInput[0]), numpy.mean(dataInput[1]), numpy.std(dataInput[1])
    #print dataSet[i]
    
print ""

for iterOutput in range(numRangeOutput):
    dataOutput = [[],[]]
    for iterInput in range(numRangeInput):
        for iterLayer in range(numRangeLayer):  
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                dataOutput[i] += eachData
    
    print iterOutput+2, numpy.mean(dataOutput[0]), numpy.std(dataOutput[0]), numpy.mean(dataOutput[1]), numpy.std(dataOutput[1])

print ""

for iterLayer in range(numRangeLayer):
    dataLayer = [[],[]]
    for iterInput in range(numRangeInput):
        for iterOutput in range(numRangeOutput):
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                dataLayer[i] += eachData
    
    print iterLayer+1, numpy.mean(dataLayer[0]), numpy.std(dataLayer[0]), numpy.mean(dataLayer[1]), numpy.std(dataLayer[1])

print ""

for iterInput in range(numRangeInput):
    for iterOutput in range(numRangeOutput):
        
        tempData = [[],[]]
        for iterLayer in range(numRangeLayer):
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                tempData[i] += eachData
        
        print iterInput+2, iterOutput+2, numpy.mean(tempData[0]), numpy.std(tempData[0]), numpy.mean(tempData[1]), numpy.std(tempData[1])

print ""
        
for iterInput in range(numRangeInput):
    for iterLayer in range(numRangeLayer):    
        
        tempData = [[],[]]
        for iterOutput in range(numRangeOutput):
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                tempData[i] += eachData
        
        print iterInput+2, iterLayer+1, numpy.mean(tempData[0]), numpy.std(tempData[0]), numpy.mean(tempData[1]), numpy.std(tempData[1])

print ""
        
for iterOutput in range(numRangeOutput):
    for iterLayer in range(numRangeLayer):    
        
        tempData = [[],[]]
        for iterInput in range(numRangeInput):
            for i, eachData in enumerate(dataSet[iterInput][iterOutput][iterLayer]):
                tempData[i] += eachData
        
        print iterOutput+2, iterLayer+1, numpy.mean(tempData[0]), numpy.std(tempData[0]), numpy.mean(tempData[1]), numpy.std(tempData[1])

# 
# 
# newList = fileOpened.readlines()
# 
# fileOpened.close()
# 
# newNames = []
# 
# for eachLine in newList:
#     listCell = eachLine.split(',')
#     dataParsing = listCell[1].split('>')
#     namePaper = dataParsing[1].split('<')
#     newNames.append(listCell[0] + ','+namePaper[0] + '\n')
#     
# fileWriteOpen = open("./referParsed.csv",'w')
# 
# for eachLine in newNames:
#     print eachLine
#     fileWriteOpen.write(eachLine)
# 
# fileWriteOpen.close()
