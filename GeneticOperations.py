import random
import copy

chroLen = 12
popu = 100
pool = [[] for _ in range(popu)]
valued = [0, 1, 8, 12, 18, 27, 36]
maxSize = 300
adjVal = 20
numberMulti = 50
extraMulti = 5

def getValSet(chro):
    val = 0
    mod = 0
    bonus = 0
    
    for item in chro:        
        val += item*item
        mod += valued[item]
        
    if mod < maxSize:
        bonus = -maxSize
    else:
        bonus = maxSize - mod
        
    maximizer = sum([numberMulti for item in chro if item == 0])
  
    return [val, bonus*extraMulti, maximizer]

def evalu(chro):
    return sum(getValSet(chro))

def cross(chro1, chro2):    
    newOne = []
    
    for idx in range(chroLen):
        if random.random < 0.5:
            newOne.append(copy.deepcopy(chro1[idx]))
        else:
            newOne.append(copy.deepcopy(chro2[idx]))
        
    return newOne
    
def mut(chro):
    newOne = copy.deepcopy(chro)
    idx = random.randint(0,chroLen-1)
    newOne[idx] = random.randint(0,len(valued)-1)

    return newOne
    
def initPool(pool):    
    for chro in pool:
        for _ in range(chroLen):
            chro.append(random.randint(0,len(valued)-1))
            
    return len(pool)

def evalPool(pool):    
    pool.sort(key = evalu, reverse = True)      
    pool = [pool[idx] for idx in range(len(pool)) if idx < popu]
    
    return len(pool)

def crossPool(pool):
    for idx in range(popu):
        chro = pool[idx]
        if random.random() < 0.7:
            partner = random.choice(pool)
            pool.append(cross(chro, partner))
            
    return len(pool)

def mutPool(pool):
    for idx in range(popu):
        chro = pool[idx]
        if random.random() < 0.8:
            pool.append(mut(chro))
    
    return len(pool)

def printBestInPool(gen, pool):    
    for i in range(1):
        print gen, i, evalu(pool[i]), getValSet(pool[i]), pool[i]
    
initPool(pool)    
for gen in range(1000):
    evalPool(pool)
    printBestInPool(gen, pool)
    crossPool(pool)
    mutPool(pool)