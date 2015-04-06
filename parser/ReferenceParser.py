
fileOpened = open("./reference.csv",'r')

newList = fileOpened.readlines()

fileOpened.close()

newNames = []

for eachLine in newList:
    listCell = eachLine.split(',')
    dataParsing = listCell[1].split('>')
    namePaper = dataParsing[1].split('<')
    newNames.append(listCell[0] + ','+namePaper[0] + '\n')
    
fileWriteOpen = open("./referParsed.csv",'w')

for eachLine in newNames:
    print eachLine
    fileWriteOpen.write(eachLine)

fileWriteOpen.close()
