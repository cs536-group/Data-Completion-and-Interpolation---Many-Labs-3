import codecs
import csv
import dataFormat as df
import pickle as pkl
import random

def saveVar(var, path, name):
    saveFile = open(path+name, 'wb')
    pkl.dump(var, saveFile)
    saveFile.close()
    return

def loadVar(path, name):
    loadFile = open(path+name, 'rb')
    var = pkl.load(loadFile)
    loadFile.close()
    return var

#code data by col
def readData(path = None, name = None):
    if path is None:
        path = 'D:/Users/endlesstory/Desktop/536/final/ML3/ML3/'
    if name is None:
        name = 'ML3AllSitesC.csv'

    file = codecs.open(path + name, 'rb', 'cp850')
    csvR = csv.reader(file, delimiter = ',')

    index = 0
    name = []
    size = 0

    formatFun = []
    realMatrix = []
    flagMatrix = []
    dataMatrix = []

    for row in csvR:
        index = index + 1
        if index == 1:
            name = row
            size = len(name)
            for col in range(size):
                if col <= 134 or 170 <= col <= 171 or 222 <= col <= 224 or 242 <= col <= 253 or 255 <= col <= 258 or 268 <= col <=270:
                    funName = 'df.data' + name[col].replace('.', '_') + '()'
                    dataFormatFun = eval(funName)
                    dataFormatFun.oriCol = col
                    formatFun.append(dataFormatFun)
                else:
                    formatFun.append(None)
        else:
            flagMatrix.append([])
            dataMatrix.append([])
            realMatrix.append([])
            rowIndex = index - 2
            for col in range(size):
                if col <= 134 or 170 <= col <= 171 or 222 <= col <= 224 or 242 <= col <= 253 or 255 <= col <= 258 or 268 <= col <=270:
                    real, flag, data = formatFun[col].formatFore(row[col])
                    realMatrix[rowIndex].append(real)
                    flagMatrix[rowIndex].append(flag)
                    dataMatrix[rowIndex].append(data)
                else:
                    realMatrix[rowIndex].append(None)
                    flagMatrix[rowIndex].append(None)
                    dataMatrix[rowIndex].append(None)

    file.close()
    return (formatFun, flagMatrix, dataMatrix, realMatrix)

#group data by test
def sortData(formatFun, flagMatrix, dataMatrix, realMatrix):
    flagSortedMatrix = []
    dataSortedMatrix = []
    realSortedMatrix = []
    posList = [0 for i in range(12)]

    for row in range(len(flagMatrix)):
        flagSorted = [[] for i in range(12)]
        dataSorted = [[] for i in range(12)]
        realSorted = [[] for i in range(12)]
        flagSortedMatrix.append(flagSorted)
        dataSortedMatrix.append(dataSorted)
        realSortedMatrix.append(realSorted)

        for col in range(len(formatFun)):
            tempFormatFun = formatFun[col]
            tempFlag = flagMatrix[row][col]
            tempData = dataMatrix[row][col]
            tempReal = realMatrix[row][col]
            if tempFormatFun is None:
                continue

            tempGroup = tempFormatFun.group
            if row == 0:
                tempFormatFun.sCol = (tempGroup, posList[tempGroup])
            if isinstance(tempFlag, list):
                if row == 0:
                    posList[tempGroup] = posList[tempGroup] + len(tempFlag)
                    tempFormatFun.eCol = (tempGroup, posList[tempGroup])
                flagSorted[tempGroup].extend(tempFlag)
                dataSorted[tempGroup].extend(tempData)
                realSorted[tempGroup].extend(tempReal)
            else:
                if row == 0:
                    posList[tempGroup] = posList[tempGroup] + 1
                    tempFormatFun.eCol = (tempGroup, posList[tempGroup])
                if col == 21 or col == 117: #(year, month)
                    if tempFlag and flagMatrix[row][244] and flagMatrix[row][222]: #YearComputer #MonthComputer
                        tempData = max(0, (dataMatrix[row][224] - tempData[0] + 2000) * 12 + (dataMatrix[row][222] - tempData[1]))
                    else:
                        tempFlag = False
                        tempData = -1
                flagSorted[tempGroup].append(tempFlag)
                dataSorted[tempGroup].append(tempData)
                realSorted[tempGroup].append(tempReal)
    return (formatFun, flagSortedMatrix, dataSortedMatrix, realSortedMatrix)


#merge row into a single list
def mergeData(flagMatrix, dataMatrix, realMatrix):
    flagMergedMatrix = []
    dataMergedMatrix = []
    realMergedMatrix = []

    for row in range(len(flagMatrix)):
        flagMerged = [x for group in flagMatrix[row] for x in group]
        if flagMerged.count(False) >= 100:
            continue
        dataMerged = [x for group in dataMatrix[row] for x in group]
        realMerged = [x for group in realMatrix[row] for x in group]
        flagMergedMatrix.append(flagMerged)
        dataMergedMatrix.append(dataMerged)
        realMergedMatrix.append(realMerged)
        if len(flagMerged) != len(dataMerged) or len(dataMerged) != len(realMerged):
            print('E: mergeData: size error at row: %d' %row)
    return (flagMergedMatrix, dataMergedMatrix, realMergedMatrix)


#compute merged col to oriCol map
def getPos(formatFun, flagList):
    posList = [len(group) for group in flagList]
    accPosList = [sum(posList[:i]) for i in range(len(posList))]
    deSortMap = dict()

    for i in range(len(formatFun)):
        tempFormatFun = formatFun[i]
        if tempFormatFun is None:
            continue
        group, shift = tempFormatFun.sCol
        tempFormatFun.sCol = accPosList[group] + shift
        group, shift = tempFormatFun.eCol
        tempFormatFun.eCol = accPosList[group] + shift

        deSortMap[tempFormatFun.sCol] = (tempFormatFun.eCol, tempFormatFun.oriCol)

    return formatFun, deSortMap


#scale data into [0, 1]
def scaleData(flagMatrix, dataMatrix):
    minDataMatrix = [float('inf') for i in range(len(flagMatrix[0]))]
    maxDataMatrix = [float('-inf') for i in range(len(flagMatrix[0]))]

    for row in range(len(flagMatrix)):
        for col in range(len(flagMatrix[row])):
            tempFlag = flagMatrix[row][col]
            if tempFlag:
                tempData = float(dataMatrix[row][col])
                dataMatrix[row][col] = tempData
                if tempData > maxDataMatrix[col]:
                    maxDataMatrix[col] = tempData
                if tempData < minDataMatrix[col]:
                    minDataMatrix[col] = tempData
            else:
                dataMatrix[row][col] = 0

    difDataMatrix = [maxDataMatrix[i] - minDataMatrix[i] for i in range(len(minDataMatrix))]

    for row in range(len(flagMatrix)):
        for col in range(len(flagMatrix[row])):
            tempFlag = flagMatrix[row][col]
            if tempFlag:
                if difDataMatrix[col] == 0:
                    if minDataMatrix[col] == 0 or minDataMatrix[col] == 1:
                        minDataMatrix[col] = 0
                    else:
                        if col == 260: #col 224 YearComputer
                            dataMatrix[row][col] = 0
                        else:
                            print(minDataMatrix[col])
                            print('W: scaleData: unnecessary data at col %d' %col)
                else:
                    dataMatrix[row][col] = (dataMatrix[row][col] - minDataMatrix[col]) / difDataMatrix[col]
    return flagMatrix, dataMatrix, minDataMatrix, difDataMatrix


#transform dataList into unsorted unmerged unscaled format, which can use formatFun.formatBack to transform into original dataset format
def restoreData(dataList, deSortMap, minDataMatrix, difDataMatrix):
    reDataList = [None for i in range(274)]
    size = len(dataList)
    col = 0
    while col < size:
        sCol = col
        eCol, oriCol = deSortMap[col]
        for tempCol in range(sCol, eCol):
            if difDataMatrix[tempCol] != 0:
                dataList[tempCol] = dataList[tempCol] * difDataMatrix[tempCol] + minDataMatrix[tempCol]
            else:
                dataList[tempCol] = dataList[tempCol] + minDataMatrix[tempCol]
        if eCol == sCol + 1:
            reDataList[oriCol] = round(dataList[tempCol])
        else:
            maxIndex = 0
            maxData = dataList[sCol]
            for i in range(0, eCol - sCol):
                if dataList[sCol + i] >= maxData:
                    maxIndex = i
                    maxData = dataList[sCol + i]
            if dataList[sCol + maxIndex] == 0:
                reDataList[oriCol] = [False for i in range(eCol - sCol)]
            else:
                for i in range(0, eCol - sCol):
                    reDataList[oriCol] = [False for x in range(eCol - sCol)]
                    reDataList[oriCol][maxIndex] = True
        col = eCol

    month = reDataList[222] - reDataList[21] % 12
    if month < 0:
        month = month + 12
        reDataList[21] = reDataList[21] + 12
    year = reDataList[224] - (reDataList[21] // 12)
    reDataList[21] = (int(year) + 2000, int(month))

    month = reDataList[222] - reDataList[117] % 12
    if month < 0:
        month = month + 12
        reDataList[117] = reDataList[117] + 12
    year = reDataList[224] - (reDataList[117] // 12)
    reDataList[117] = (int(year) + 2000, int(month))
    return reDataList


def decodeData(dataList, formatFun):
    size = len(formatFun)
    decodedData = [None for i in range(size)]
    for col in range(size):
        tempFormatFun = formatFun[col]
        if tempFormatFun is None:
            continue
        if isinstance(dataList[col], list):
            flag = [True for i in range(len(dataList[col]))]
        else:
            flag = True
        decodedData[col] = tempFormatFun.formatBack((flag, dataList[col]))

    return decodedData

#transform restoredData to original dataset format
def splitData(flagMatrix, dataMatrix, realMatrix):
    trainFlag = []
    trainData = []
    trainReal = []
    testFlag = []
    testData = []
    testReal = []
    validFlag = []
    validData = []
    validReal = []
    for row in range(len(flagMatrix)):
        setIndex = random.random()
        if setIndex < 0.8:
            trainFlag.append(flagMatrix[row])
            trainData.append(dataMatrix[row])
            trainReal.append(realMatrix[row])
        elif setIndex < 0.9:
            testFlag.append(flagMatrix[row])
            testData.append(dataMatrix[row])
            testReal.append(realMatrix[row])
        else:
            validFlag.append(flagMatrix[row])
            validData.append(dataMatrix[row])
            validReal.append(realMatrix[row])
    return  (trainFlag, trainData, trainReal, testFlag, testData, testReal, validFlag, validData, testReal)




if __name__ == '__main__':
    formatFun, flagMatrix, dataMatrix, realMatrix = readData()
    formatFun, flagSortedMatrix, dataSortedMatrix, realSortedMatrix = sortData(formatFun, flagMatrix, dataMatrix, realMatrix)

    formatFun, deSortMap = getPos(formatFun, flagSortedMatrix[0])

    flagMergedMatrix, dataMergedMatrix, realMergedMatrix = mergeData(flagSortedMatrix, dataSortedMatrix, realSortedMatrix)
    flagScaledMatrix, dataScaledMatrix, minDataMatrix, difDataMatrix = scaleData(flagMergedMatrix, dataMergedMatrix)
    splitedData = splitData(flagScaledMatrix, dataScaledMatrix, realMergedMatrix)

    saveVar(formatFun, 'D:/Users/endlesstory/Desktop/536/final/data/', 'formatFun.pkl')
    saveVar(flagScaledMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'flagScaledMatrix.pkl')
    saveVar(dataScaledMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'dataScaledMatrix.pkl')
    saveVar(realMergedMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'realScaledMatrix.pkl')
    saveVar(deSortMap, 'D:/Users/endlesstory/Desktop/536/final/data/', 'deSortMap.pkl')
    saveVar(minDataMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'minDataMatrix.pkl')
    saveVar(difDataMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'difDataMatrix.pkl')
    saveVar(splitedData, 'D:/Users/endlesstory/Desktop/536/final/data/', 'splitedData.pkl')