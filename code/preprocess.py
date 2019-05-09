import codecs
import csv
import dataFormat as df

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
                if col <= 134:
                    funName = 'df.data' + name[col].replace('.', '_') + '()'
                    formatFun.append(eval(funName))
        else:
            flagMatrix.append([])
            dataMatrix.append([])
            rowIndex = index - 2
            for col in range(size):
                if col <= 134:
                    flag, data = formatFun[col].formatFore(row[col])
                    flagMatrix[rowIndex].append(flag)
                    dataMatrix[rowIndex].append(data)

            if index > 20:
                break



    print(flagMatrix)
    print(dataMatrix)

    file.close()
    return

#66 69 95 102 116

if __name__ == '__main__':
    readData()