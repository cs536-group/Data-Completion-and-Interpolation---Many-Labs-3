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
            rowIndex = index - 2
            for col in range(size):
                if col <= 134 or 170 <= col <= 171 or 222 <= col <= 224 or 242 <= col <= 253 or 255 <= col <= 258 or 268 <= col <=270:
                    flag, data = formatFun[col].formatFore(row[col])
                    flagMatrix[rowIndex].append(flag)
                    dataMatrix[rowIndex].append(data)
                else:
                    flagMatrix[rowIndex].append(None)
                    dataMatrix[rowIndex].append(None)

    file.close()
    return (formatFun, flagMatrix, dataMatrix)

#group data by test
def sortData(formatFun, flagMatrix, dataMatrix):
    flagSortedMatrix = []
    dataSortedMatrix = []
    posList = [0 for i in range(12)]

    for row in range(len(flagMatrix)):
        flagSorted = [[] for i in range(12)]
        dataSorted = [[] for i in range(12)]
        flagSortedMatrix.append(flagSorted)
        dataSortedMatrix.append(dataSorted)

        for col in range(len(formatFun)):
            tempFormatFun = formatFun[col]
            tempFlag = flagMatrix[row][col]
            tempData = dataMatrix[row][col]
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
    return (formatFun, flagSortedMatrix, dataSortedMatrix)


#merge row into a single list
def mergeData(flagMatrix, dataMatrix):
    flagMergedMatrix = []
    dataMergedMatrix = []

    for row in range(len(flagMatrix)):
        flagMerged = [x for group in flagMatrix[row] for x in group]
        if flagMerged.count(False) >= 100:
            continue
        dataMerged = [x for group in dataMatrix[row] for x in group]
        flagMergedMatrix.append(flagMerged)
        dataMergedMatrix.append(dataMerged)
        if len(flagMerged) != len(dataMerged):
            print('E: mergeData: size error at row: %d' %row)
    return flagMergedMatrix, dataMergedMatrix


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
                dataList[tempCol] = round(dataList[tempCol] * difDataMatrix[tempCol] + minDataMatrix[tempCol])
            else:
                dataList[tempCol] = round(dataList[tempCol] + minDataMatrix[tempCol])
        if eCol == sCol + 1:
            reDataList[oriCol] = dataList[tempCol]
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


def splitData(flagScaledMatrix, dataScaledMatrix):
    trainFlagScaled = []
    trainDataScaled = []
    testFlagScaled = []
    testDataScaled = []
    validFlagScaled = []
    validDataScaled = []
    for row in range(len(flagScaledMatrix)):
        setIndex = random.random()
        if setIndex < 0.8:
            trainFlagScaled.append(flagScaledMatrix[row])
            trainDataScaled.append(dataScaledMatrix[row])
        elif setIndex < 0.9:
            testFlagScaled.append(flagScaledMatrix[row])
            testDataScaled.append(dataScaledMatrix[row])
        else:
            validFlagScaled.append(flagScaledMatrix[row])
            validDataScaled.append(dataScaledMatrix[row])
    return  (trainFlagScaled, trainDataScaled, testFlagScaled, testDataScaled, validFlagScaled, validDataScaled)


if __name__ == '__main__':
    formatFun, flagMatrix, dataMatrix = readData()
    formatFun, flagSortedMatrix, dataSortedMatrix = sortData(formatFun, flagMatrix, dataMatrix)

    formatFun, deSortMap = getPos(formatFun, flagSortedMatrix[0])

    flagMergedMatrix, dataMergedMatrix = mergeData(flagSortedMatrix, dataSortedMatrix)
    flagScaledMatrix, dataScaledMatrix, minDataMatrix, difDataMatrix = scaleData(flagMergedMatrix, dataMergedMatrix)
    splitedData = splitData(flagScaledMatrix, dataScaledMatrix)

    saveVar(formatFun, 'D:/Users/endlesstory/Desktop/536/final/data/', 'formatFun.pkl')
    saveVar(flagScaledMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'flagScaledMatrix.pkl')
    saveVar(dataScaledMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'dataScaledMatrix.pkl')
    saveVar(deSortMap, 'D:/Users/endlesstory/Desktop/536/final/data/', 'deSortMap.pkl')
    saveVar(minDataMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'minDataMatrix.pkl')
    saveVar(difDataMatrix, 'D:/Users/endlesstory/Desktop/536/final/data/', 'difDataMatrix.pkl')
    saveVar(splitedData, 'D:/Users/endlesstory/Desktop/536/final/data/', 'splitedData.pkl')


    # resData = restoreData(dataScaledMatrix[0], deSortMap, minDataMatrix, difDataMatrix)
    # print(resData)
    # print(dataMatrix[2])