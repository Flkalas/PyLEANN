import copy
import itertools


smaller = set([i for i in range(10)])
sameone = set([i for i in range(10)])
larger = set([i for i in range(20)])

print smaller.issubset(larger)
print larger.issubset(smaller)
print smaller.issubset(sameone)

for compareSet in itertools.combinations(smaller,2):
    print list(compareSet), smaller
    if 3 in list(compareSet):
        pass
#         smaller.remove(3)
        
for compareSet in itertools.combinations([i for i in range(5)],2):         
    print list(compareSet)
     
for compareSet in itertools.combinations(range(5),2):         
    print list(compareSet)
    
# setList = set()
# setList.add(set(range(2)))
# print setList
# setList.add(set(range(3)))
# print setList
# setList.add(set(range(2)))
# print setList


oneList = list()
print oneList
oneList.append([0,1])
oneList.append([1,2])
oneList.append([2,3])
oneList.append([3,0])
oneList.append([0,2])
oneList.append([1,3])
print oneList
print "\n\n\n"



        
def getCliquesN(adMat,sizeClique):            
    if sizeClique < 3:
        return []
    
    n = len(adMat)
    
    listClique3 = []
    
    for i in range(n):
        firstConnected = [j for j in range(i+1,n) if adMat[i][j]]
        for compareSet in itertools.combinations(firstConnected,2):
            compareSet = list(compareSet)
            if adMat[compareSet[0]][compareSet[1]]:
                compareSet.append(i)
                listClique3.append(sorted(compareSet))
        
    if sizeClique < 4:
        return listClique3
    
    listCliqueN = [listClique3]
                
    for i in range(sizeClique-3):
        hasLargerClique = [False for _ in range(n)]
        listLargerClique = []                
        
        for j, eachClique in enumerate(listCliqueN[i]):
            for k in range(eachClique[i+2]+1,n):                        
                isLarger = True
                                        
                for eachIndex in eachClique:                    
                    if not adMat[eachIndex][k]:
                        isLarger = False                        
                        break
                    
                if isLarger:
                    largerClique = copy.deepcopy(eachClique)
                    largerClique.append(k)
                    listLargerClique.append(sorted(largerClique))

        if len(listLargerClique) > 0:
            listCliqueN.append(listLargerClique)
        else:
            break
                
        for largerClique in listLargerClique:
            for setLowerClique in itertools.combinations(largerClique,i+3):
                for j, eachClique in enumerate(listCliqueN[i]):                    
                    if list(setLowerClique) == eachClique:
                        hasLargerClique[j] = True
                        break
        
        newListCliqueN = []
        for j, eachDelete in enumerate(hasLargerClique):
            if not eachDelete:
                newListCliqueN.append(listCliqueN[i][j])
        listCliqueN[i] = newListCliqueN
    
    listMergingCluque = []
    for eachCliqueN in listCliqueN:
        for eachClique in eachCliqueN:
            listMergingCluque.append(eachClique)
                
    return listMergingCluque
    
sizeLayer = 4
adMat = [[False for _ in range(sizeLayer)] for _ in range(sizeLayer)]
        
for eachListUniqueness in oneList:
    adMat[eachListUniqueness[0]][eachListUniqueness[1]] = True
    adMat[eachListUniqueness[1]][eachListUniqueness[0]] = True

print getCliquesN(adMat, sizeLayer)


newList = range(10)
print newList
print newList == range(10)



