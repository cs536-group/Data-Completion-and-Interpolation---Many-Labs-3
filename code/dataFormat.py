import re

class dataCol(object):
    def __init__(self):
        # self.numIMap = dict()
        # self.numOMap = dict()
        # self.codeIMap = dict()
        # self.codeOMap = dict()
        self.type = 'unknown' #data type
        self.oriCol = None #original dataset col
        self.group = None #test group, 0 for all
        self.sCol = None #coded dataset group start col
        self.eCol = None #coded dataset group end col
        self.real = None #real value flag
        return

    def numFore(self, iData):
        return iData

    def numBack(self, oData):
        return oData

    def codeFore(self, iData):
        return (iData, iData, iData)

    def codeBack(self, oData):
        flag, data = oData
        return data

    def formatFore(self, iData):
        return self.codeFore(self.numFore(iData))

    def formatBack(self, oData):
        return self.numBack(self.codeBack(oData))

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return 'column %d (%d: %d): ' %(self.oriCol, self.sCol, self.eCol) + self.__class__.__name__ + ': ' + self.type

#multiple choice
class dataChoice(dataCol):
    def __init__(self):
        super(dataChoice, self).__init__()
        self.type = 'str / int / [bool\'s]'

        self.numIMap = dict()
        self.numOMap = dict()
        self.iMapSize, self.oMapSize = self._getMapSize()
        self.defaultNum = 0
        self.mapLowerCase = False
        self.real = False
        return

    def _getMapSize(self):
        return (len(self.numIMap), len(self.numOMap))

    def numFore(self, iData):
        if self.mapLowerCase:
            iData = iData.lower()
        if iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return self.defaultNum

    def numBack(self, oData):
        return self.numOMap[oData]

    def codeFore(self, iData):
        size = self.iMapSize
        data = [self.real for i in range(size)]
        realFlag = [False for i in range(size)]
        if iData == 0:
            flag = [False for i in range(size)]
        else:
            flag = [True for i in range(size)]
            data[iData - 1] = True
        return (realFlag, flag, data)

    def codeBack(self, oData):
        flag, data = oData
        size = self.oMapSize - 1
        for i in range(size):
            if data[i]:
                return i+1
        else: #no valid data
            for i in range(size):
                if flag[i]: #flag is valid
                    print('W: ' + repr(self) + ', codeBack: invalid oData at col %d' %self.oriCol)
                    return 0
            else:
                return 0

#positive int for ID
class dataPosInt(dataCol):
    def __init__(self):
        super(dataPosInt, self).__init__()
        self.type = 'str / int / int'
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag is True:
            return data
        else:
            return -1

#true answer
class dataTrueAnswer(dataCol):
    def __init__(self):
        super(dataTrueAnswer, self).__init__()
        self.type = 'str / int / bool'
        self.iAns = ''
        self.oAns = ''
        self.real = False
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        elif iData.lower() == self.iAns:
            return 1
        else:
            return 0

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        elif oData == 1:
            return self.oAns
        else:
            return 'notTrueAnswer'

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag is True:
            return round(data)
        else:
            return -1

#natural language
class dataNaturalLanguage(dataCol):
    def __init__(self):
        super(dataNaturalLanguage, self).__init__()
        self.type = 'str / int / bool'
        self.real = False
        return

    def numFore(self, iData):
        return int(iData != 'NA') 

    def numBack(self, oData):
        if oData == 0:
            return 'NA'
        else:
            return 'someString'

    def codeFore(self, iData):
        if iData == 0:
            return (self.real, False, False)
        else:
            return (self.real, True, True)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return 0


#NA or valid
class dataBool(dataCol):
    def __init__(self):
        super(dataBool, self).__init__()
        self.type = 'str / int / bool'
        self.validStr = ''
        self.real = False
        return

    def numFore(self, iData):
        return int(iData != 'NA') 

    def numBack(self, oData):
        if oData == 0:
            return 'NA'
        else:
            return self.validStr

    def codeFore(self, iData):
        if iData == 0:
            return (self.real, False, False)
        else:
            return (self.real, True, True)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return 0

#int choice
class dataInt(dataPosInt):
    def __init__(self):
        super(dataInt, self).__init__()
        self.minInt = 0
        self.invalid = ''
        return

    def numFore(self, iData):
        if iData == self.invalid:
            return -1
        else:
            return int(iData) - self.minInt

    def numBack(self, oData):
        if oData == -1:
            return self.invalid
        else:
            return str(oData + self.minInt)



#0
class dataSite(dataChoice):
    def __init__(self):
        super(dataSite, self).__init__()
        self.numIMap = {'AshlandUniversity': 1, 'BradleyUniversity': 2, 'CarletonUniversity': 3,
                        'IthacaCollege': 4, 'MiamiUniversity': 5, 'MichiganStateUniversity': 6,
                        'MontanaStateUniversity': 7, 'NA': 0, 'NovaSoutheasternUniversity': 8,
                        'OSUNewark': 9, 'PacificLutheranUniversity': 10, 'PennStateAbington': 11,
                        'SanDiegoStateUniversity': 12, 'TexasAandM': 13, 'UCDavis': 14,
                        'UCRiverside': 15, 'UniversityOfFlorida': 16, 'UniversityOfSouthernMississippi': 17,
                        'UniversityOfToronto': 18, 'UniversityOfVirginia': 19, 'VirginiaCommonwealthUniversity': 20}

        self.numOMap = {1: 'AshlandUniversity',  2: 'BradleyUniversity',  3: 'CarletonUniversity',
                        4: 'IthacaCollege',  5: 'MiamiUniversity',  6: 'MichiganStateUniversity',
                        7: 'MontanaStateUniversity',  0: 'NA',  8: 'NovaSoutheasternUniversity',
                        9: 'OSUNewark',  10: 'PacificLutheranUniversity',  11: 'PennStateAbington',
                        12: 'SanDiegoStateUniversity',  13: 'TexasAandM',  14: 'UCDavis',
                        15: 'UCRiverside',  16: 'UniversityOfFlorida',  17: 'UniversityOfSouthernMississippi',
                        18: 'UniversityOfToronto',  19: 'UniversityOfVirginia',  20: 'VirginiaCommonwealthUniversity'}
        self.iMapSize, self.oMapSize = self._getMapSize()

        self.group = 11
        return

#1
class dataParticipant_ID(dataPosInt):
    def __init__(self):
        super(dataParticipant_ID, self).__init__()
        self.group = 11
        return

#2
class dataRowNumber(dataPosInt):
    def __init__(self):
        super(dataRowNumber, self).__init__()
        self.group = 11
        return

#3
class datasession_id(dataPosInt):
    def __init__(self):
        super(datasession_id, self).__init__()
        self.group = 11
        return

#4 @all
class dataage(dataCol):
    def __init__(self):
        super(dataage, self).__init__()
        self.type = 'str / int / int'

        self.numIMap = {'NA': -1, '18 almost 19': 19, '22 years': 22, 'almost 19': 19, 'Too Old (18)': 18, '18 years': 18,
                        '19.5': 19, '20`': 20, 'we': -1, '-2': -1, 'almost 18': 18, '17 (18 in one month)': 18}
        
        self.group = 0
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            oData = int(iData)
            if oData >= 100:
                return -1
            else:
                return int(iData)
        else:
            if iData in self.numIMap:
                return self.numIMap[iData]
            else:
                return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#5 @persistance @test4
class dataanagrams1(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams1, self).__init__()
        self.iAns = 'party'
        self.oAns = 'party'
        self.group = 4
        return

#6 @persistance @test4
class dataanagrams2(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams2, self).__init__()
        self.iAns = 'fatal'
        self.oAns = 'fatal'
        self.group = 4
        return

#7 @persistance @test4
class dataanagrams3(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams3, self).__init__()
        self.iAns = None
        self.oAns = 'notAWord'
        self.group = 4
        return

#8 @persistance @test4
class dataanagrams4(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams4, self).__init__()
        self.iAns = None
        self.oAns = 'notAWord'
        self.group = 4
        return

#9 ~@test3
#anyway, maybe it reflects some traits about this person
class dataattention(dataChoice):
    def __init__(self):
        super(dataattention, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}

        self.iMapSize, self.oMapSize = self._getMapSize()

        self.group = 0
        return

    def codeBack(self, oData):
        flag, data = oData
        size = self.oMapSize - 1
        for i in range(size):
            if data[i]:
                return i+1
        else: #no valid data
            return 0

#10 ~@test3
class dataattentioncorrect(dataChoice):
    def __init__(self):
        super(dataattentioncorrect, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, 'I read the instructions': 1, 'I read the instructions!': 1, 'i read the instructions': 1, 'I read instructions': 1,
                        'Ice Skating': 0, 'I read the instructions.': 1, 'go out for walk and hang out with my friends': 0, 'I read the Instructions': 1,
                        'Spend time with friends': 0, 'going out': 0, 'i read the intstructions': 1, 'all of the above': 0, 'I read the instuctions': 1,
                        'I read the intructions': 1, 'I read these instructions': 1, 'I read the instructions....after I Clicked': 1, 'Playing with my Baby': 0,
                        'I read the instructions" after the \'other\' option below. Thank you very much.': 1, 'I read the insrtuctions': 1, 'Hang out with friends': 0,
                        'I read the intsructions': 1, 'I read the instructions (but accidentally clicked a bubble)': 1, 'I read the instructions (accidently clicked on that first)': 1,
                        'smoking weed': 0, 'I READ THE GOD DAMN INSTRUCTIONS': 1, 'I READ THE INSTRUCTIONS': 1, 'i read the directions': 1, 'self improvement': 0,
                        'spending time with family': 0, 'I read the instructions. I choose my preference by accident before I read the instructions. Sorry.': 1,
                        'i read da instuctionz': 1, 'being with friends': 0, 'Internet': 0, 'watching movies,shopping': 0, 'I will read the instructions': 1,
                        'i readthe instructions': 1, 'i READ THE INSTRUCTIONS': 1, 'I red the instructions': 1, 'I read the directions': 1,
                        'I read the instructions after choosing an answer': 1, 'I read the intrsuctions': 1, 'I read the instruction': 1, 'I read theinstructions': 1,
                        'Eating, sleeping': 0, 'Sleeping': 0, 'hanging out with friends, working, reading and relaxing': 0, 'I Read the Instructions': 1,
                        'I have read the instructions': 1, 'I read the insructions': 1, 'i read the instruction': 1, 'GEEETAR': 0, 'I READ THE INSTRUCTIONS.': 1,
                        'i read instructions': 1, 'I read the instructions, accidentally clicked on way to the box': 1, 'soccer': 0,
                        'I read the instructions but jumped the gun on answering the question': 1, 'I read the instructions Haha I read them.': 1, 'I read the isructions': 1,
                        'i have read the instructions': 1, 'playing soccer with friends': 0, 'SLEEPING,DOING CHORES, DOING WORK': 0, 'drawing, painting': 0, 'sleeping': 0,
                        'I read the directions, afterwards.': 1, 'I read the istructions': 1, 'work': 0, 'i read the intructions': 1, 'all of these': 0,
                        'Play sports, watch tv, exercise, cook.': 0, "I read the instructions... after I already chose an answer, and it won't let me deselect it.": 1,
                        'I read the instructions after clicking...': 1, 'video games': 0, 'I': 0, 'Being with friends': 0, 'I read the intstructions': 1, 'All the above!': 0,
                        'I read the instructions after clicking': 1, 'I read the instructions :)': 1, 'I read the instructions. But I also like eating.': 1,
                        'I read  the instructions': 1, 'Exercising': 0, 'i read the instrucions': 1, 'Spending time with friends': 0, 'I read the instructions...but i also chose': 1,
                        'communicating with friends': 0, 'I read the instructions but I clicked an option by accident.': 1, 'I read the instructions, but I still clicked one.': 1,
                        'spending time with my family': 0, 'I read the instructions but still felt like answering the question anyways': 1, 'drawing': 0,
                        'Hanging out with friends': 0, 'study': 0, 'play games with friends': 0, 'i read the instructions.': 1, 'photograhpy': 0, "I didn't read the instructions.": 1,
                        'I read the instructions (and clicked accidentally)': 1, 'I read the instructions, but only after I had already chosen something from the list.': 1,
                        'I read the instructions...After I clicked on the preferences. Sorry.': 1, 'Did not read the last part but went back after...': 1,
                        "I play for the VCU Women's Soccer team.": 0, 'I have read the Insturctions': 1, 'I read the instructions, mostly.': 1, 'surfing': 0}
        self.numOMap = {-1: 'NA', 1: 'I read the instructions', 0:'worngAnswer'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 3
        self.defaultNum = 0

        self.group = 3
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag is True:
            return round(data)
        else:
            return -1

#11 @test5
class databackcount1(dataTrueAnswer):
    def __init__(self):
        super(databackcount1, self).__init__()
        self.iAns = '357'
        self.oAns = '357'
        self.group = 5
        return

#12 @test5
class databackcount10(dataTrueAnswer):
    def __init__(self):
        super(databackcount10, self).__init__()
        self.iAns = '330'
        self.oAns = '330'
        self.group = 5
        return

#13 @test5
class databackcount2(dataTrueAnswer):
    def __init__(self):
        super(databackcount2, self).__init__()
        self.iAns = '354'
        self.oAns = '354'
        self.group = 5
        return

#14 @test5
class databackcount3(dataTrueAnswer):
    def __init__(self):
        super(databackcount3, self).__init__()
        self.iAns = '351'
        self.oAns = '351'
        self.group = 5
        return

#15 @test5
class databackcount4(dataTrueAnswer):
    def __init__(self):
        super(databackcount4, self).__init__()
        self.iAns = '348'
        self.oAns = '348'
        self.group = 5
        return

#16 @test5
class databackcount5(dataTrueAnswer):
    def __init__(self):
        super(databackcount5, self).__init__()
        self.iAns = '345'
        self.oAns = '345'
        self.group = 5
        return

#17 @test5
class databackcount6(dataTrueAnswer):
    def __init__(self):
        super(databackcount6, self).__init__()
        self.iAns = '342'
        self.oAns = '342'
        self.group = 5
        return

#18 @test5
class databackcount7(dataTrueAnswer):
    def __init__(self):
        super(databackcount7, self).__init__()
        self.iAns = '339'
        self.oAns = '339'
        self.group = 5
        return

#19 @test5
class databackcount8(dataTrueAnswer):
    def __init__(self):
        super(databackcount8, self).__init__()
        self.iAns = '336'
        self.oAns = '336'
        self.group = 5
        return

#20 @test5
class databackcount9(dataTrueAnswer):
    def __init__(self):
        super(databackcount9, self).__init__()
        self.iAns = '333'
        self.oAns = '333'
        self.group = 5
        return

#21 @test9
class databestgrade1(dataCol):
    def __init__(self):
        super(databestgrade1, self).__init__()
        self.type = 'str / (int, int) / (int, int)'
        #refer to stanford
        self.numIMap = {'NA': (-1, -1), 'Spring 2014': (2014, 6), '14-May': (2014, 5), 'spring 2014': (2014, 6), 'spring 2013': (2014, 6), 'Winter 2008': (2008, 3), 'Fall 2013': (2013, 12),
                        'Winter 2014': (2014, 3), 'Senior in High School': (-1, -1), 'Spring 2013': (2013, 6), 'Sping 2014': (2014, 3), 'Spring 2012': (2012, 6), 'Winter 2013': (2013, 3),
                        'Fall 2014': (2014, 12), 'High school senior': (-1, -1), 'Summer 2014': (2014, 8), 'fall 2014': (2014, 12), 'spring 2005': (2005, 6), 'winter 2013': (2013, 3),
                        'Before starting at Bradley, Spring 2014': (2014, 6), 'summer of 2014': (2014, 8), '14-Jun': (2014, 6), 'summer 2014': (2014, 8), 'winter 3013': (2013, 3),
                        'summer 2013': (2013, 8), 'winter 2014': (2014, 3), 'spring 14': (2014, 6), 'Prior to the current term? Spring 2014': (2014, 6), 'fall 2010': (2010, 12),
                        'NA (First term)': (-1, -1), 'highschool 2014': (-1, -1), 'Summer, 2014': (2014, 8), 'Summer 2013': (2013, 8), 'Winter 2012': (2012, 3),
                        'Winter and Fall 2014 (present)': (2014, 3), 'fall 2011': (2011, 12), 'winter2014': (2014, 3), 'winter 2014 (high school)': (2014, 3),
                        'June 2014 (High School)': (2014, 6), 'summer 4014': (2014, 8), 'Current - so last term was Spring 2014': (2014, 6),
                        "Spring 2014 (if you don't count the current term)": (2014, 6), 'spring of 2014': (2014, 6), 'high school 21014': (-1, -1), 'Spring 2014.': (2014, 6),
                        'Fall, 2014': (2014, 12), 'Currently still in school. Last full term was High School Fall of 2013-Spring 2014.': (2014, 6),
                        'sping 2014': (2014, 3), 'Fall 2017': (-1, -1), 'Spring 2015': (-1, -1), 'Now: Fall 2014': (2014, 12), 'Now (Fall 2014)': (2014, 12),
                        'currently in school so, Fall 2014': (2014, 12), "Fall '14": (2014, 12), 'currently': (-1, -1), '(High School) Spring 2014': (2014, 6), 'Fall 2015': (-1, -1),
                        'currently in school, last completed term Spring 2014': (2014, 6), 'Spring  2013': (2013, 6), 'spring2014': (2014, 6),
                        'This is my first semester at MSU. So my last term would my senior year of high school': (-1, -1),
                        'currently in school (Fall 2014)': (2014, 12), 'Spring2014': (2014, 6), 'Summer 2014#': (2014, 8), 'WINTER2012': (2012, 3), 'High school Spring 2014': (2014, 6),
                        'Spring 14': (2014, 6), 'Winter 2011': (2011, 3), 'spring 2011': (2011, 6), 'fall 2013': (2013, 12), 'Senior year - final semester': (-1, -1), 'spring 2010': (2010, 6),
                        '2014': (-1, -1), 'sophmore': (-1, -1), 'winter 2007': (2007, 3), 'Spring 2011': (2011, 6), 'FALL 2014': (2014, 12), 'fall 2008': (2008, 12), 'Spring 2014 (High School)': (2014, 6),
                        'SPRING 2014': (2014, 6), 'Fa;; 2-14': (2014, 12), 'winter2013': (2013, 3), 'winter 2008': (2008, 3), 'High school': (-1, -1), 'summer2014': (2014, 8), '13-May': (2013, 5),
                        'winter 2103': (2013, 3), 'current': (-1, -1), 'Fall 2014 (freshman)': (2014, 12), 'I am currently in school.': (-1, -1), 'fall2012': (2012, 12),
                        'Fall 2014(current)': (2014, 12), '5': (-1, -1), 'this is my first semester i graduated high school in 2012': (-1, -1), 'Autumn 2014': (2014, 12),
                        'Autum 2014': (2014, 12), 'currently in school. autum 2014': (2014, 12), 'autumn 2014': (2014, 12), 'Currently': (-1, -1), 'spring 2104': (2014, 6),
                        'high school': (-1, -1), 'This year:Winter 2014. Before that, Summer 2010': (2014, 3), 'High School 2012': (-1, -1),
                        'winter 2013, high school, i am a freshman at Newark': (2013, 3), 'Autum 14': (2014, 12), 'this is my first term': (-1, -1),
                        'spring 2014 for high school': (2014, 6), '14-Aug': (2014, 8), 'n/a': (-1, -1), '20 minutes ago.': (-1, -1), 'AUTUMN 2014': (2014, 12), '2013': (-1, -1),
                        'i was still in high school': (-1, -1), 'fall': (-1, -1), "I finished high school in June of 2014, so I haven't completed a whole term yet.": (-1, -1),
                        'Autumn 13': (2013, 12), 'now...': (-1, -1), 'may,spring 2014': (2014, 5), '26 hours ago': (-1, -1), 'WINTER 2014': (2014, 5), '14-Sep': (2014, 9), 'fall 20143': (-1, -1),
                        'Spring 2014 and currently': (2014, 6), 'High School so N/A?': (-1, -1), "I'm in school right now..": (-1, -1), 'spirng 2014': (2014, 6),
                        'Spring Semester 2014': (2014, 6), '(Spring 2014)': (2014, 6), 'Spring 2014 (High school)': (2014, 6), 'Spring 2014 (Currently in Fall 2014)': (2014, 6),
                        'Fall': (-1, -1), 'Spring': (-1, -1), '2010': (-1, -1), 'Spring 2014 (not including this term)': (2014, 6), 'spring 1997': (-1, -1), 'Fall 14': (2014, 12),
                        'Spring 204': (2014, 6), 'FAll 2014': (2014, 12), 'high school 2012': (-1, -1), 'high school 2014': (-1, -1), 'LAST SEMESTER': (-1, -1), '12th Grade': (-1, -1),
                        'sping2013': (2013, 3), 'Summer of 2013': (2013, 8), 'sep. 2013- jun. 2014': (2014, 6), 'Summer 2012': (2012, 8), 'spin 2014': (2014, 6), 'Summer 1 & 2 2014': (2014, 8),
                        'Spring 2001': (-1, -1), 'spring 201': (-1, -1), 'Summer & Fall 2014': (2014, 12), 'spring 2014 (high school)': (2014, 6), 'Fall2014': (2014, 12), 'Winter 1998': (-1, -1),
                        'FAll 2011': (2011, 12), 'Fall 2014 (Currently in school)': (2014, 12), 'Winter 2009': (2009, 3), 'The last term I was in school was the Spring of 2014': (2014, 6),
                        '13-Mar': (2013, 3), 'High School, Spring 2014': (2014, 6), 'Currently enrolled': (-1, -1), 'sPRING 2014': (2014, 6), 'winter 2013 - high school': (2013, 3),
                        'FALL2014': (2014, 12), 'This term, Fall 2014': (2014, 12), 'SPRING  2014': (2014, 6), 'Spring 201A': (-1, -1), 'Currently in school': (-1, -1),
                        'Spring 2013, last year - high school': (2013, 6), 'Summer Session 2 2014': (2014, 8), 'High School': (-1, -1), 'summer 2018': (-1, -1),
                        'spring 2015': (-1, -1), '2014 summer': (2014, 8), 'Summer Session II 2014': (2014, 8), 'Summer Session 1': (2014, 8), 'high school spring semester 2014': (2014, 6),
                        'Summer session 2 2014': (2014, 8), '2013 Fall': (2013, 12), 'Second Semester (High School, Senior Year)': (-1, -1), 'Summer Session 1 2014': (2014, 8),
                        'Summer session II': (-1, -1), 'SUMMER 2014': (2014, 8), 'Summer Session 2': (-1, -1), 'summer 14': (2014, 8), 'Summer2014': (2014, 8), 'summer': (-1, -1),
                        'Spring Quarter 2014': (2014, 6), 'Semester 2 2014': (2014, 6), 'Spring 2104': (2014, 6), 'fall 2014 is my first term': (2014, 12), 'SPRING 20114': (2014, 6),
                        "This is my first quarter. I'm a freshman": (-1, -1), 'Fall 2012': (2012, 12), 'This is my first term. Fall 2014.': (2014, 12), 'Summer B 2014': (2014, 8),
                        "I'm a freshman now so Highschool spring 2014": (2014, 6), "spring'14": (2014, 6), 'WINTER 2013': (2013, 3), 'Spring 2014 (Last Semester of High school)': (2014, 6),
                        'Fall 2010': (2010, 12), '41760': (-1, -1), '(spring14)': (2014, 6), 'spring': (-1, -1), 'spring 2012': (2012, 6), 'High school 2013-2014': (-1, -1), 'winter 2012': (2012, 3),
                        'Winter/Spring 2014': (2014, 6), 'Spring/Summer 2014 in Highschool': (2014, 8), 'February-July 2014': (2014, 7), '41852': (-1, -1), 'high school, June 2014': (2014, 6),
                        'Spring/Summer 2014': (2014, 8), "If you don't count now - fall 2014, then spring 2014.": (2014, 6), 'Winter 2013 (High School)': (2013, 3),
                        'Not counting this current semester, Spring 2014': (2014, 6), 'currently in school': (-1, -1), 'Currently in school.': (-1, -1),
                        'senior year of high school': (-1, -1), 'Spring 2014-present': (2014, 12), 'not counting this term, Spring 2013': (2013, 6),
                        'Fall 2014 (First year student)': (2014, 12), 'Srping 2014': (2014, 6), 'Winter 2013-2014': (2014, 3), '2013-2014 highschool': (-1, -1),
                        'Fall, 2014 (still in session), if this means last full term: Spring, 2014': (2014, 6), 'sring 2014': (2014, 6),
                        'winter of 2014 in high school': (2014, 3), 'Spring/Summer 2013': (2013, 8), '1 hour ago': (-1, -1), 'Fall 2013?': (2013, 12), 'an hour ago': (-1, -1)}
        
        self.group = 9
        self.real = True
        return

    def numFore(self, iData):
        if iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return (-1, -1)

    def numBack(self, oData):
        if oData == (-1, -1):
            return 'NA'
        else:
            return '%d %d' %(oData[1], oData[0])

    def codeFore(self, iData):
        if iData == (-1, -1):
            return (self.real, False, (0, 0))
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return (-1, -1)

#22 ~@test9
class databestgrade2(dataCol):
    def __init__(self):
        super(databestgrade2, self).__init__()
        self.type = 'str / int / int'
        #refer to https://www.rapidtables.com/calc/grade/gpa-to-letter-grade-calculator.html
        self.numIMap = {'na': -1, 'a - 97%': 97, 'c': 76, 'c-': 72, 'b': 86, 'a': 96, '94': 94, 'a+': 100, '98': 98, 'b+': 89, '99%': 99, 'c+': 79, '98%': 98, 'gpa was a 3.2': 89, 'b-': 82,
                        'a plus': 100, '100%': 100, '88%': 88, 'psychology': -1, 'a-': 92, '93': 93, '87% b': 87, 'physics': -1, '92%': 92, 'pre-calculus, with a low d': 66, 'f': 59,
                        '83': 83,'math': -1, '90%': 90, 'd': 66, '80': 80, '82%': 82, '100': 100, '86': 86, '90': 90, '91%': 91, '103%': 103, '67%': 67, '75': 75, 'withdrawn': -1, '72%': 72,
                        'na (first term)': -1, '88': 88, '60%': 60, '78': 78, '92': 92, '91': 91, '68': 68, '89%': 89, '85': 85, 'competent (c)': 73, '78%': 78, '60': 60, '79%': 79,
                        '70%': 70, '70': 70, '107': 107, '75%': 75, '89': 89, '104': 104, '3.5': 92, '74': 74, '84': 84, '81': 81, '96': 96, '103': 103, '97%': 97, '76': 76, '95%': 95, '3.33': 89,
                        'for spring 2014: 98%': 98, '105%': 105, 'chemistry- 88%': 88, '97': 97, '2': 76, '77%': 77, '74%': 74, '80%': 80, '2.5': 82, '4': 96, '4.0-a': 96, '1.5': 72,
                        'i have not received grades yet for fall 2014 but in the past the worst grade i had gotten would have been a b+.': 89, 'cse iss mth stt  3.0': 86,
                        'e': 59, '69%': 69, 'general business b+': 89, '79': 79, '3': 86, '86%': 86, '3.5 (85%)': 85, 'gpa 3.5': 92, '85%': 85, '96%': 96, '4.0- a': 96, '94%': 94,
                        '112.98%': 113, 'a (95%)': 95, '93%': 93, '71%': 71, '0': 59, 'withdraw': -1, 'b+ 88%': 88, 'chemistry,90': 90, '#name?': -1, '83%': 83, '87': 87, '76%': 76, '101.5': 102,
                        '95': 95, '57%': 57, 'high school (a+)': 100, '82': 82, 'd-': 62, '66%': 66, '99': 99, '2.8': 86, 'like a 85': 85, '90% english': 90,
                        'had to pass/fail a math course, 61%': 61, 'c mabye?': 76, 'government': -1, 'my best final grade was a 100%': 100, '3.3': 89, "a's": 96, 'n/a': -1,
                        '108%': 108, 'freshman': -1, 'b, in ap english.': 86, '90 percent': 90, '58%': 58, 'c 78%': 78, 'w': -1,
                        'the best grade i got last year my senior year was an a': 96, '72': 72, 'educational psychology': -1, 'freshman this semester': -1, 'english 97': 97,
                        '73': 73, 'my best final grade was an 92% in psychology': 92, "as'": 96, 'summer: a': 96, '84%': 84, 'i believe it was a 64': 64, '65%': 65, '1': 66,
                        '65': 65, 'my best final grade was an a-': 92, 'a-97%': 97, '+c': 79, 'history': -1, 'high scool 97%': 97, 'a-92': 92,
                        'still on my first semester, but so far chemistry': -1, 'havent yet': -1, 'med micro': -1, '0.83': 83, '89.9': 90, '0.32': 32, 'd+': 69, '3.9': 96, '0.91': 91,
                        '0.75': 75, '0.98': 98, '0.76': 76, '0.82': 82, '0.95': 95, '0.79': 79, '0.88': 88, '0.86': 86, '0.9': 90, '0.56': 56, '~90%': 90, '0.85': 85,
                        'my best grade was an 89%.': 89, 'a (94%)': 94, '0.5': 50, '0.87': 87, 'n/a in high school, b.': 86, 'c 70%': 70, '0.94': 94, '0.65': 65, 'b +': 89, '0.7': 70,
                        '3.83': 96, '0.93': 93, 'a- to b+': 89, '0.99': 99, '100% a': 100, "n/a i'm an incoming freshman": -1, '85 b': 85, '3.2': 89, '0.798': 80, '105': 105, '0.6': 60,
                        '66': 66, '0.92': 92, '0.68': 68, '0.89': 89, '77': 77, '0.8': 80, '0.96': 96, '49': 49, '67': 67, '42104': -1, '0.45': 45, '0.23': 23, '63': 63, '0.78': 78, '0.77': 77,
                        'this is my first semester': -1, '90% in ap statiscs': 90, '87%': 87, 'economics a-': 92, 'politics of the middle east': -1, 'n/a (first year student)': -1,
                        '0.905': 91, '0.97': 97, '1.02': 102, 'got an a on my voice jury.': 96}
        
        self.group = 9
        self.real = True
        return

    def numFore(self, iData):
        iData = iData.lower()
        if iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#23 @test9
class databestgrade3(dataPosInt):
    def __init__(self):
        super(databestgrade3, self).__init__()
        self.group = 9
        return

#24 @test9
class databestgrade4(dataPosInt):
    def __init__(self):
        super(databestgrade4, self).__init__()
        self.group = 9
        return

#25 @test9
class databestgrade5(dataPosInt):
    def __init__(self):
        super(databestgrade5, self).__init__()
        self.group = 9
        return

#26 @test4
class databig5_01(dataPosInt):
    def __init__(self):
        super(databig5_01, self).__init__()
        self.group = 4
        return

#27 @test4
class databig5_02(dataPosInt):
    def __init__(self):
        super(databig5_02, self).__init__()
        self.group = 4
        return

#28 @test4
class databig5_03(dataPosInt):
    def __init__(self):
        super(databig5_03, self).__init__()
        self.group = 4
        return

#29 @test4
class databig5_04(dataPosInt):
    def __init__(self):
        super(databig5_04, self).__init__()
        self.group = 4
        return

#30 @test4
class databig5_05(dataPosInt):
    def __init__(self):
        super(databig5_05, self).__init__()
        self.group = 4
        return

#31 @test4
class databig5_06(dataPosInt):
    def __init__(self):
        super(databig5_06, self).__init__()
        self.group = 4
        return

#32 @test4
class databig5_07(dataPosInt):
    def __init__(self):
        super(databig5_07, self).__init__()
        self.group = 4
        return

#33 @test4
class databig5_08(dataPosInt):
    def __init__(self):
        super(databig5_08, self).__init__()
        self.group = 4
        return

#34 @test4
class databig5_09(dataPosInt):
    def __init__(self):
        super(databig5_09, self).__init__()
        self.group = 4
        return

#35 @test4
class databig5_10(dataPosInt):
    def __init__(self):
        super(databig5_10, self).__init__()
        self.group = 4
        return

#36 ~@test5
class datadiv3filler(dataCol):
    def __init__(self):
        super(datadiv3filler, self).__init__()
        self.type = 'str / int / bool'
        #16 = 10 = 1 mod 3
        self.numIMap = {'NA': -1, '3 9 6 9 6 3 3 9': 1, '1,3,6,9': 0, '3 9 6 9 3 3 9': 1, '3,9,6': 1, '3 9 6': 1, '3,9,6,9,6,3,3,9': 1, '3,6,9': 1,
                        '6,9': 1, '3,9,6,1': 0, '3, 9, 6, 63': 1, '3, 9, 6, 9, 6, 3, 3, 9': 1, '3 9 6 9 4 3 3 9': 0, '3,9,6,96,3,3,9': 1,
                        '3,9,63,90,24,18,36,12,15,30': 1, '3, 9, 6': 1, '9,9,63,9': 1, '90, 3, 321, 21, 3213': 1, '3 90696339': 1, '3,9,89,63,90,92': 0,
                        '3, 9, 0, 6,': 1, '3, 9, 6, 90, 46, 63': 0, '3, 6, 9, 12, 15, 18, 21, 24, 27, 30,': 1, '3 6 9 63 5890': 0, '3, 9, 6, 90, 63': 1,
                        '3 6 9 63': 1, '3 6 9': 1, '3,9': 1, '9,89,9,6,63,3,3,9': 0, '3,9,90,26,68,63': 0, '3,9,6,': 1, '3, 90,63,6, 9': 1, '3 9': 1, '3 9 63': 1,
                        '3, 9, 6, 9, 63, 6, 3, 3, 9': 1, '9 89 63 3': 0, '3 9 0 6 9 6 3 3 9': 1, '9 6 9 6 3 3 9': 1, '3,9,6,90,63': 1, '3, 90, 9, 44, 6,': 0,
                        '3,90,226,89,89,446,463,63,9': 0, '3,9,89,90,6': 0, '3,9,6,63,90': 1, '3 9 9 3 9': 1, '3, 5890, 89, 4463, 92, 8848': 0, "3,6,9's": 1,
                        '3 9 9 6 63 3 3 9': 1, '32,268': 0, '9, 6, 3': 1, '3,6,9,26,63': 0, '3, 89, 90, 68': 0, '3, 6, 9': 1, '3,9,6,63': 1, '3,6,9,63': 1,
                        '3 9 0 1 6 3 3 9': 0, '3,9,63,90': 1, '3, 9, 90, 6, 9, 6, 3, 63, 3, 9,': 1, '3,3,3,6,6,9, 63': 1, '3, 9, 6, 9, 6, 9': 1, '3,9,90,63': 1,
                        '3 589 89 4463 3': 0, '3.59E+20': 0, '3,9,6,9,3,3,9': 1, '9,3 6': 1, '3 1 9 6 9 3 3 9': 0, '3 2268 9 6': 1, '3,9,6,9,6,63,9': 1, '3,9,90': 1,
                        '3, 2268, 44633': 0, '3,9,0,6,9,90,': 1, '3,5,9,6,9,3,3,9': 1, '3, 90, 63, 93, 69, 213, 3213, 27': 1, '3 2268': 1, '3, 6, 9,': 1, '3, 9, 90, 6': 1,
                        '3 9 6 1': 0, '3,9,90,2268,6,633,33': 1, '3, 9, 0, 6, 9, 6, 3, 3, 9': 1, "Everything is divisible by 3, I'll assume you mean whole integers. 3, 9, 6, 9, 6, 3, 3, 9,": 1,
                        '3, 9, 6, 9, 3, 3, 9': 1, '3, 6, 9, 90, 63, 33': 1, '3 9 9 6 3 3 9': 1, '1 3 6 9': 0, '3 63': 1, '3,9,0,6,9,6,3,3,9': 1, '3,9,6,63,': 1,
                        '3, 90, 2268, 63': 1, '3,9,9,6,3,3': 1, '9,3,6': 1, "integers - 3, 9, 6 fractional answers for the rest.  Letters don't count?": 1, '3BB8B92': 0,
                        '3, 9, 0, 6, 9, 3, 3, 9': 1, '3,9,63,9,93,69,6,21,27,84': 1, '3, 9, 6, 63, 3,': 1, '9,6,3': 1, '3 9 0 6': 1, '3, 9, 0, 6': 1, '3,9,6,9, 6,3,3,9,': 1,
                        '3, 9, 90, 9, 6, 63, 9': 1, '3. 6, 9': 1, '9 6': 1, '3, 9, 6, 9. 6, 3, 3, 9': 1, '9, 3. 89, 63, 90': 0, '3 3 6 9 6 9 9 3': 1, '0,3, 3, 3, 6, 6, 9, 9, 9': 1,
                        '3,5,8,9,2,2,6,8,8,9,1,7,4,4,6,3,3,8,9,2': 0, '3,6,9,36': 1, '3.59E+14': 0, '3, 9, 6, 9, 6, 3, 9': 1, '63, 3, 90,': 1, '3,9,3': 1, '3, 9': 1, '6 9 3': 1,
                        '3,9,90,2268,27,321,3213': 1, '3,1': 0, '3,458,904,226,818,920,000,000,000,000,000,000,000,000,000,000,000': 0, '3, 9, 6,': 1, '3 589 2268 3': 0,
                        '3,3,3,9,9,9,6,6': 1, '63 3': 1, '3, 6, 9, 63': 1, '3 9 3 9': 1, '3,6,9,6,3,3,9': 1, '3,90,9,3,3,9': 1, '3 9 6 63 90 69 27 84': 1, '3, 0, 6, 9': 1,
                        '3, 89, 4463,': 0, '3,9,6,9,3,6,3,9': 1, '3, 2268, 3': 1, '3,9,6,9,6,3,9': 1, '3B8917B44633B': 1, '3, 9,63': 1, '3,89,4463,3': 0, '3, 3213, 27': 1,
                        '3 90 6 63': 1, '3,9,24,15,18,21,27,33': 1, '3 9 6 9 6 3 9': 1, '3,9,63,90, 92': 0, '3,9,6,90,2268': 1, '3,9,0,6': 1, '3, 9, 90, 6, 63': 1, '3,6,9,': 1,
                        '3, 9, 6, 9, 3, 3, 9,': 1, '3,8,6,9,3,6,3,9': 0, '3, 9, 89, 92, 589': 0, '3 9 9 3 3 9': 1, '9 6 3': 1, '3 9 9 3 6 3 9': 1, '9 90 93 63 69 3 21 27 39': 1,
                        '3,99,9,6,9': 1, '3,6,9, 90, 63,': 1, '3,63,89': 0, '3,9,6,9,6,3,3,9,': 1, '3, 9, 6, 9, 6,3, 3,9': 1, '9, 6, 890,63': 0, '3,9, 89': 0, '3,9,90,2268,9,63,3,3,9': 1,
                        '3, 9, 6, 1': 0, '3, 9, 90, 6, 68, 63': 0, '3, 9, 26, 226, 92, 63': 0, '3,9,0,6,0,6,0,3,9': 1, '3,1,3,3': 0, '3,9,0,6,63,90,589,2268,': 0, '3 9 6 6 3 9 3': 1,
                        '3 9 6 9 9 3 3 9': 1, '3,58,90,2268, 93, 321, 63, 869, 213': 0, '3, 9, 9,3,3,9': 1, '1,2,3,4,5,6,7,8,9,0': 0, '3, 6, 9, 90, 63,': 1, '3,9,90,6,9,6,3,63,3,9': 1,
                        '30; 90; 882; 744; 174;': 1, '3/9/06': 1, '3 9 6 2': 0, '3,9, 6, 9, 6, 3, 3, 9': 1, '3,9,63,6,33,': 1, '3, 5890,': 0, '3, 9 , 6, 63, 90': 1, '3,6,9,90, 63,': 1,
                        '3, 9, 589, 89, 90, 890, 46, 463, 4463,': 0, '3, 9, 6, 90, 2268, 63': 1, '1,1963.3,756,29.67,5.6,1488,1,2.67,30.67': 0, '3, 6, 9, 63, 90': 1, '3 9 0 6 9 1 6 3 3 9': 0,
                        '3 9 3 9 1 6 3 3 9': 0, '3, 9, 0, 6, 90, 2268, 63': 1, '3 6  9': 1, '3, 8,9,6,': 0, '3 9 90 63 6': 1, '3 6 9 12 15 18 21 24': 1, '3 9 6 9 6 3 3': 1, '3, 9, 0, 6, 4463': 0,
                        '1,3,9': 0, '3 9 1 6': 0, '3, 9, 6, 6, 3, 3, 9 (All of the numbers in the table are technically divisible by 3, though these are the only ones that create whole numbers.)': 1,
                        'B54891': 0, '3,8917, 4463, 92': 0, '9 3': 1, '3,58,90,63,3': 0, '3 90 6 9 63': 1, '3,9,63': 1, '3, 63, 9, 6': 1, '1,3,9,6': 0, '3, 9, 90, 6, 89, 63,': 0,
                        '9,6,9,6,3,3,9': 1, '3,9,6,27': 1, '3,9,6,9,3,3': 1, '9,6': 1, '6, 9': 1, '6,9,3': 1, '3,9,6,9,1,6,3,3': 0, '3,6,9,63,90': 1, '9 6 9 3 3 9': 1, '9,6,3,': 1,
                        '3,9,17': 0, '3 9 6 6 3 9': 1, '3 9 63 90': 1, '3, 9, 6, 90, 89, 5890, 63, 4463, 44633, 463, 4633, 633, 890': 0, '3 9 6 869 27': 0, '3 9 90 6 93 63 69 96': 1,
                        '3,92': 0, '3,8,0,6,9,6,3,3,9': 0, '3,9,9,1,6,3,3,9': 0, '9, 3,6': 1, '3 9 6 9 3 46 89 9 21': 0, '9,6,3,90,63': 1, '3 9 9 6 6 3 3 9': 1, '3,9,6,89,': 0,
                        '3 9 6 9 3 6 3 3 9': 1, '3, 63, 90': 1, '358,944,633': 0, '3, 9,90,63,6': 1, '3,6,9, 90, 2268, 63': 1, '3 90 3': 1,
                        '3,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,90,96,99': 1, '3,9,90,9,6,63,3,3,9': 1, '3,9,,9,3,3,9': 1,
                        '1, 9, 6, 90, 63,': 0, '3, 6, 9. 90, 63': 1, '3, 9, 6, 6, 3, 3, 9,': 1, '3 9 90 6': 1, '3 9 6 9 6 2 9': 0, '3,6,9,12,15,18,21,24,27,30,33,36,': 1,
                        '3 9,6': 1, '3,6,9,63, 89': 0, '3, 9, 89, 90, 63': 0, '9, 6, 9, 6, 3, 3, 9': 1, '1, 3, 6, 9': 0, '3,6,9,63,90,2268': 1, 'there are none': 1,
                        '3, 9, 6, 9, 6, 3, 9, 63': 1, '3,9,6,9,6,': 1, '3; 9, 6; 9; 6; 3; 3; 9': 1, '3 9 6 90 63': 1, '3,9,6,46, 92, 226, 2268': 0, '3,9,9,6,3,3,9': 1, '9, 6': 1,
                        '3,9,3,6,9,6,3,9': 1, '3, 2268, 3,': 1, '0,3,6,9,': 1, '1 3 9': 0, '0, 3, 6, 9, 12, 21, 27, 36, 39, 48, 63, 69, 72, 84, 90, 96,': 1, '3, 6,9': 1, '3,6,9,90,63': 1,
                        '3, 6, 9, 64,': 0, '3,2268,': 1, '3 9 0 2 2 6 9 1 6 3 3 8 9 2': 1, '3 5 8 9 2 2 6 8 9 1 7 4 4 6 3 3 8 9 2': 1, '3 5 6 8 9': 0, '3, 5890, 4463': 0, '1,3,6,9,63,90': 1,
                        '3,9,6,63,92,90,27,93,69,21': 0, '9, 6, 9, 6, 9': 1, '3, 9, 6, 589, 268, 2268, 63': 0, '3 9 90 63 3 92': 0, '9 6 9 6 9': 1, '3, 9, 0, 6,9,6,9': 1, '9,2,1': 0,
                        '3 5 8 9 0 2 6 1 7 4': 1, '3 9 6 9 6 3': 1, '3,9,68,3,92': 0, '3,9,90,6,9,6,63,3,9': 1, '9 3 6': 1, '3,9,6,9,6,3,3,9.': 1, '3,9,90,6,63,33,633': 1,
                        '3 89 9 9 6 3 63 3 9': 0, '3 9 589 89 226 26 6 4463 446 46': 0, '3, 1, 6, 9': 0, '3 9 6 9 6 9': 1, '3 6 9 6 3 3 9': 1, '3, 9, 6, 63, 26': 0,
                        '3, 9, 6, 9, 6, 3, 3, 9,': 1, '3,5,8,9,0,2,6,1,7,4': 1, '3,6,9,63,46,': 0, '3 9 6 9 9': 1, '3,9,0,6,1': 0, '3 89 4463': 0, '9,9,89,63,6,92': 0,
                        '3,3.5,16,6,10,3': 0, '3,6,9,89,589,4463': 0, '3, 9, 63': 1, '3, 9, 6, 9, 3, 9': 1, '3,589,89,4463,3': 0, '6 9': 1, '3, 9, 89, 63, 3, 9, 6': 0,
                        '3, 6, 2268, 9, 33,': 1, '3,5890,89,4463,3,92': 0, '3 9 9 6 3 6 3 9': 1, '3, 9, 6, 9, 6, 3, 3, 9.': 1, '3,6,9,1': 0, '3 6 9 12 21 27': 1,
                        '3, 89, 92, 4463': 0, '3, 9,6,9,6,3,3,9': 1, '3, 6 , 9 , 90 , 63 ,16 ,': 0, '3 9 6 9 6 3 9 3 9': 1, '3,6,9,63,90,': 1, '9 90': 1, '3, 90, 6, 9, 63, 3, 9': 1,
                        '3,9,589,89,4463,92': 0, '89,89,63,9': 0, '3, 9, 0, 6, 9,6, 3, 9,': 1, '3,6,9,44633': 0, '3 2268 3': 1, '3 6 9 90 63': 1, '3 6 9 68 63': 0, '3, 1, 9': 0,
                        '3 90 63': 1, '3, 9, 6, 90,': 1, '1,3': 0, '3,9, 6, ,9, 6, 3, 3, 9': 1, '3 9 0 6 90 63 633': 1, '9,6,3,1': 0, 'Assuming here that 3 can go into itself... 3,9,6,9,6,3,3,9': 1,
                        '3 9 90': 1, '0 3 6 9': 1, '3 9 9 6 3 6 9 3': 1, '3, 1': 0, '3,6, 9, 2268': 1, '3,9, 90, 63': 1, '3, 9, 30, 39, 9, 69, 96, 6, 3, 63, 3, 9, 39, 93,': 1,
                        '3,9,58,89,63': 0, '3 9 9 6 63 3 9': 1, '3 9 0 6 9 3 9': 1, '3,6,9,90': 1, '3; 9; 0; 6; 9; 6; 3; 3; 9': 1, '6,12,18,24,30,3,9,33,60,90': 1, '3,9,6,6,9,6,3,3,9': 1,
                        '6,9,12,15,18,21,24,27,30,33,36,...': 1, '2268B89': 0, '6, 9, 9, 8, 7, 6, 5': 0, '3 9 90 6 63 3 3 9': 1, '3,6,9,90,': 1, '39289B6BB': 0,
                        '3, 5, 8, 9, 2, 2, 6, 8, 8, 9, 1, 7, 4, 4, 6, 3, 3, 8, 9, 2': 0, '3 9 6  90 2268 63': 1, '3,9,6,6,3,3,9': 1, '3,9,63,': 1,
                        '3 9 90 321 3213 213 21 2268 9 6 6 3 3 9 27 84 48 69 93': 1, '3, 9, 90, 6, 9, 63, 6, 3, 3, 9': 1, '5.89E+18': 0, '3 9 90 63': 1, '3 9 6 90 26': 0,
                        '3,90,63,6,9': 1, '3,9,90,6': 1, '3,9,6,90,63,': 1, '3 9 90 6 63': 1, '3 589 89 9 90 226 63': 0, '3 9 6 63 90': 1, '3,9,90,2268,89,9,63,3,9': 0, '3 9 89 63': 0,
                        'all the numbers are divisible by 3. The evenly divisible, single digit numbers are 3,6,9.': 1, '9,9,6,,9,': 1, '3, 9, 6, 63, 2268': 1, '3, 9, 9, 3, 3, 9': 1,
                        '3 9 6 0 6 3 9': 1, '3,9,6,9,6,3,6,3,3,9': 1, '3 9 6 9 6 3 6 3 3 9': 1, '3,58,90,63,33,39': 0, '3 9 6 63': 1, '3 9 90 6 9 6 3 63 3 9': 1, '3, 9, 6, 63,': 1,
                        '3, 9, 6, 58,63,': 0, '3 9 0 9 3 2 9': 0, '3,6,9,63,89': 1, '3,9,90,6,63': 1, '3 5890 8917': 0, '3, 9, 9, 6, 3, 3, 9': 1, '3,90,6,9,63,3,9': 1, '3, 9, 63, 90': 1,
                        '3 9 6 9 6 3 3 2': 0, 'b5b': 1, '3,4463,3': 0, '9,27,36,63,90,58': 0, '3,9,6,9,6,1,1,9': 0, '3 9 6 63 90 2268': 1, '3, 2268': 1, '5890, 4463': 0, '9,6,9,3,3,3,9': 1,
                        '3,9,6,0': 1, '3 9 6 0': 1, '3. 9, 6, 9, 6, 3, 3, 9': 1, '3,6,9,6,3,3': 1, '9,9,6,9,6,3,3,3': 1, '3,2268,3': 1, '3, 6, 9, 92, 63,': 0, '89, 9, 90, 6, 89, 6, 63, 3, 3, 9': 0,
                        '3,9,6,9,63,9': 1, '3,9,90,63,21,48,93,84': 1, '3B92': 0, '3,9,6,63,90,2268,': 1, '3, 9, 90, 6,': 1, '3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51': 1, '3,9,21,63,93,27,321': 1,
                        '3, 9, 0,9, 6, 3, 3 , 9': 1, '3,3,3,9,9,9': 1, '3 9 6 0 6 3 3 9': 1, '3 58 9 90 63': 0, '9,3,0,6': 1, '9,6,63': 1, '3,9,90,27,18,12,99': 1, '3 9 9 6 9 9 9': 1, '3,9,6,2268': 1,
                        '3, 9, 90, 46, 63, 3': 0, '3, 6, 9,63': 1, '3 9 0 6 9 90 63': 1, '3.69E+20': 1, '3 9 4 9 9 3 3 9': 0, '3 6 9 21 27 81 33 63 84 12 90 30 60': 1, '3,90,9,68,21,84,93,69': 0,
                        '3, 9, 6, 90, 63,': 1, '3,9,89,90,63,6': 0, '3,  9, 6, 89, 4463': 0, '3^x x=any real number': 0, '3, 6, 9, 0': 1, '3,9,6,89,63': 0,
                        '3,9, 90 ,9, 6, 3, 63, 3, 9, 93, 69, 96, 27, 72, 21': 1, '5.89E+17': 0, '3,9,2268': 1, '3,6,9, 63, 90': 1, '3, 9, 6, 9 6, 3, 3, 9': 1, '3, 9, 6, 90,63,': 1,
                        '3, 9, 90, 6, 9, 6, 63, 3, 9': 1, '6,15,24,27,0': 1, '3,9,6,9,6,6,6,9': 1, '3, 9, 6, 58, 90, 5890, 68, 63,': 0, '3,9,9,3,3,9': 1, '3 9 12 18 24 30 33 36 6 72 81': 1,
                        '3,9,1269,96,18,90': 1, '3B5887B 2268B86 17B4460 3BB8B89': 0, '3,9,6,9': 1, '3 9 89 4463 6 63 890 46': 0, '3, 21, 27, 63': 1, '3 9 63 89 69 21': 0, '0,3,6,9': 1,
                        '3,9,6,6,6,9': 1, '3,9,6,9,6,3,3,9,2': 0, '1,3,6,9,12': 0, '3, 6, 63, 89, 4463, 92': 0, '0 1 3 9': 0, '3,9,6,4463,63': 0, '3 6 9 2268': 1, '3,9,6,9,3,9': 1,
                        '3 5 8 9 2 6 8 9 1 7 4 4 6 3 8 9 2': 0, '8 2 8 7 6 8 2': 0, '3,9,6,3,6,3,3,9': 1, '3,8,6,9,6,9': 0, '3, 9, 90': 1, '3, 9, 89, 446, 63,': 0,
                        '3 5 8 9 6 8 8 9 7 4 4 6 3 3 8 9 2': 1, '3,9,90,26,63': 0, '3, 9, 6, 9, 90, 6, 3, 63, 3': 1, '3,9,2268,63,90': 1, '3,6, 9': 1, '3,4,8,9,0,2,6,1,7,5': 1,
                        '3,9,0,6,9,6,3': 1, '3 6 9 6 3 9': 1, '3 5890 2268': 0, '3,6,9,90,63,': 1, '3,6,9,2268,891,33,633,63': 1, '3,9,90,,63': 1, '3,9, 6, 63,': 1, '3,9,0,1': 0,
                        '3,9,89,63,4463,226': 0, '3,90, 39, 9, 63, 92': 0, '9, 6, 63, 90,': 1, '3, 4463': 0, '3, 9, 90, 2268, 9, 63, 9': 1, '3 6 9 92 63 90': 0,
                        '6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60': 1, '39 69 63 39': 1, '3, 2268, 9, 6': 1, '3 9 90 9 6 3 63 3 9': 1, '3,9,0': 1,
                        '3,5,8,9,2,2,6,8,8,9,1,7,4,4,6,3,3,8,9,2. You can divide all of them by 3.': 0, '6 3 9': 1, '3 9 6 9 6 9 3 3': 1, '0 1 3 6 9': 0,
                        '3,9,6,3B5890B,2268B89,17B4463,3BB8B92,63,90': 0, '3,6,9,12,18,21,24,28,30': 0, '3, 9. 0, 6, 9, 6, 3, 9': 1, '3 9  0 6': 1, '3, 9, 6, 9, 6, 3, 9, 90, 63': 1,
                        '3,8,6,9,6,3,2,9': 0, '3,9,90,6,2268,63,33': 1, '3 and 9': 1, '3, 9, 6, 589, 5890, 2268': 0, '3,9, and 6': 1, 'm': 0, '3,6,9,63,92': 0, '3,9,90,63,3,': 1,
                        '3, 9, 58, 589, 5890, 2268, 6, 63': 0, '3, 9, 6, 9, 1, 6, 3, 3, 9': 0, '3 8 6': 0, '0,3,9,6': 1, '3,3,3,6,6,9,9,9': 1,
                        '3,9,6,3,3,9 or 3,2268 ?': 1, '3,9,90,63,6,': 1,'3,5,8,9,0,2,2,6,8,8,9,1,7,4,4,6,3,3,8,9,2': 0,
                        '3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99,102, 105, 108': 1,
                        '3, 9, 90, 6, 9, 2268, 9, 63, 3, 9': 1, '9,90,63': 1, '3,9,6,9,1,3,3,9': 0, '3,9,90,6,9,6,63,6,3,9': 1, '3, 9, 90, 6, 63,': 1,
                        '122333445 6678888999 BBBBBBB': 0, '0, 3, 6, 9,': 1, '3, 9, 6, 58, 89, 90, 63': 0, '0,1,2,3,4,5,6,7,8,9': 0, '9,1,3,6': 0, '3 9 6 9 3 9': 1,
                        '9,3,3,9,90,6': 1, '3,9,90,6,3,63,3,9': 1, '3,9,90,6,9,6,3,3,9': 1, '3, 27, 9': 1, '3,6,9,0': 1, '9, 6, 90, 63': 1, '3, 9, 6, 9,6,3,3,9': 1,
                        '3,90,63,': 1, '3 6 9 12 15 18 21 24 27 30': 1, '9 9 6 3 3 9': 1, '3B5890B 3BB8B92': 0, '3 9 2268 63': 1, '1 3 9 90 63 6': 1, '3, 9,6': 1,
                        'B5890B': 0, '3,3': 1, '3,9,6,9,6,3,3': 1, '3 90 9 6 63 44': 0, '3, 6, 9, 2268': 1, '3,6,9,63,90,5890': 0, '3 B 5 8 9 0 B': 0,
                        '3 63 9 21 27 90': 1, '3 9 6  63': 1, '3,6,9,12, 15, 18, 21,24, etc.': 1, '3 9 3 6 9 6 3 3 9': 1, '3, 9, 6,2268': 1, '3, 9, 4463': 0,
                        '2268B89 17B4462': 0, '3 9 27 21 6 63 81 90': 1, '3, 9, 6, 63, 90, 0': 1, '3, 9, 6.': 1, '3, 9, 90, 9, 6, 3, 63, 3, 9': 1, '3,89,9,90,26,89,63,21,27,69.': 0,
                        '3 9 0 6 90 63': 1, '3, 21, 9, 86, 6, 63, 93, 27, 56, 89, 90, 26.': 0, '3, 90, 9, 21, 63': 1, '3,9,0,6,3,3,9': 1, '3, 9, 6, 9, 3,6, 3, 9': 1, '9,6,9,6,9': 1,
                        '3, 6, 63, 90': 1, '3, 90, 268, 63,': 0, '3,9,90,6,9,6,3,63,3,9,27': 1, '3 6 9 12 21 27 90 36 39 44 63 69 72 81 84 93 96': 0, '3,9,6,9,6,9,3': 1, '3,8,6,9,6,3,3,9': 0,
                        '9, 0, 3, 6,': 1, '3, 9,  6,': 1, '3,6,9,9,6,3,9': 1, '3,9,9,63,6,3,3,9': 1, '358 902 268 891 744 633 892': 0, '3, 9, 6,9,6,3,3,9': 1, '3,9,6,63,92': 0, '3 9696339': 1,
                        '3,9,90,6,63,21,93,96,39,72,12': 1, '3, 5890, 44633': 0, '3, 6, 9, 63, 92': 0, '3,9,1,6': 0, '3, 9, 63, 90, 69': 1, '3, 9,6,9,3,3,9': 1, '63,48,27,321,848,8848,69,869': 0,
                        '9, 3, 6': 1, '3, 3': 1, '3, 9, 9, 3, 3': 1, '3, 5890, 89, 63, and 3': 0, '3, 8, 6, 9, 6, 3, 9': 0, '9,90,8,33': 0, '3,6,9,2268': 1, '3, 9, 90, 27, 48, 69, 93': 1,
                        '3,9,90,6,2268,9,63,3,9': 1, '3, 9, 63, 589, 2268': 0, '3,9, 90, 2268, 9, 63, 3, 9': 1, '3,9,': 1, '3, 9, 6, 89, 90, 63,': 0, '3, 9, 89, 63,': 0, '3,9,9,6,6,3,3,9': 1,
                        '3, 90, 8, 63, 3, 9': 0, '3,9,90,6,2268,63': 1, '3 9 6 90 23 5890': 0, '18, 6, 30,10, 12, 4, 1': 0, '3, 90, 9, 63': 1, '3, 9, 6, 589, 226, 89, 463': 0,
                        '3 9  90 2268 6 891 9 6 63 633 33 9': 1, '3 89 63': 0, '9B': 0, '3 6 90 63 12 9 93 39': 1, '90 63 46': 0, '3,9,6,,90,': 1, '3 6 9 90': 1, '3,9,90,': 1,
                        '9 6 9 6 3 9': 1, '9,3,1,6': 0, '3,9,63,93,3213,8848': 1, '9, 6, 9, 9': 1, '3,9,226,89,63': 0}
        self.numOMap = {-1: 'NA', 1: 'numbersDivisibleBy3', 0:'worngAnswer'}

        self.group = 0
        self.real = False
        return

    def numFore(self, iData):
        if iData.isdigit():
            return (((int(iData) % 3) + 1) % 2)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        return self.numOMap[oData]

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#37 @test8
class dataelm_01(dataPosInt):
    def __init__(self):
        super(dataelm_01, self).__init__()
        self.group = 8
        return

#38 @test8
class dataelm_02(dataPosInt):
    def __init__(self):
        super(dataelm_02, self).__init__()
        self.group = 8
        return

#39 @test8
class dataelm_03(dataPosInt):
    def __init__(self):
        super(dataelm_03, self).__init__()
        self.group = 8
        return

#40 @test8
class dataelm_04(dataPosInt):
    def __init__(self):
        super(dataelm_04, self).__init__()
        self.group = 8
        return

#41 @test8
class dataelm_05(dataPosInt):
    def __init__(self):
        super(dataelm_05, self).__init__()
        self.group = 8
        return

#42 @demographics
class dataethnicity(dataChoice):
    def __init__(self):
        super(dataethnicity, self).__init__()
        #TODO: a better classification
        self.numIMap = {'na': 0, '7': 7, '6': 6, 'arab': 8, 'asian': 8, 'biracial': 7, '2': 2, '1': 1, 'mixed, half filipina': 7, '4': 4, 
                        'white & hispanic': 4, 'middle eastern': 8, 'pakistani canadian': 8, '3': 3, 'filipino': 8, 'white & east indian': 8, 'bosnian/iranian': 8, 
                        'caucasian & spanish': 8, '5': 5, 'caymanian': 8, 'european/african': 8, 'african': 8, 'asia': 8, 'haitian-american': 8, 'west indian': 8,
                        'indian-sikh': 8, 'carribean': 8, 'middle-eastern': 8, 'jamaican': 8, 'puerto rican and african american': 8, 'arbian': 8, 'indian': 8, 'haitian': 8,
                        'american': 8, 'egyptian': 8, 'hispanic': 4, 'white, hispanic/latino': 4, 'asian / white': 8, 'guatemalan': 8, 'indian,russian,greek': 7,
                        'brazilian and polish': 7, 'european': 8, 'white and asian': 7, 'south asian': 8, 'mexican': 8, 'north african': 8, 'chinese': 8,
                        'japanese': 8, 'mostly white': 7, 'korean': 8, 'bengali': 8, 'hispanic and white': 4, 'guyanese, fijian': 8, 'armenian': 8,
                        'asian- indian': 8, 'asian- international': 8, 'iranian': 8, 'half caucasian, half east asian': 7, 'black caribbean': 8, 'persian': 8,
                        'italian': 8, 'turkish': 8, 'half chinese, half iranian': 7, 'southeast asian - filipino': 8, 'sephardic jew': 8, 'both chinese and caucasian': 7,
                        'greek': 8, 'afghan': 8, 'indian - american(india)': 5, 'middle eastren': 8}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 9
        self.defaultNum = 8
        self.mapLowerCase = True

        self.group = 0
        return

#43 @test1
class datafeedback(dataBool):
    def __init__(self):
        super(datafeedback, self).__init__()
        self.validStr = 'This Stroop task has no feedback'
        self.group = 11

#44 @demographics
class datagender(dataChoice):
    def __init__(self):
        super(datagender, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '19': 3, 'Agender': 4, '3': 3, 'Gender Fluid': 4, 'gender neutral': 4, 'Alien': 4}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 5
        self.defaultNum = 4

        self.group = 0
        return

#45 @test5
class datahighpower(dataNaturalLanguage):
    def __init__(self):
        super(datahighpower, self).__init__()
        self.group = 11
        return

#46 ~@test4
class datainstructbig5(dataBool):
    def __init__(self):
        super(datainstructbig5, self).__init__()
        self.validStr = '1'
        self.group = 11
        return

#47 ~@all
class datainstructintrinsic(dataBool):
    def __init__(self):
        super(datainstructintrinsic, self).__init__()
        self.validStr = '1'
        self.group = 11
        return

#48 @? maybe related to mood?
class datainstructmli(dataBool):
    def __init__(self):
        super(datainstructmli, self).__init__()
        self.validStr = '1'
        self.group = 11
        return

#49 ~@all 
class datainstructnfc(dataBool):
    def __init__(self):
        super(datainstructnfc, self).__init__()
        self.validStr = '1'
        self.group = 11
        return

#50 @all
class dataintrinsic_01(dataPosInt):
    def __init__(self):
        super(dataintrinsic_01, self).__init__()
        self.group = 0
        return

#51 @all
class dataintrinsic_02(dataPosInt):
    def __init__(self):
        super(dataintrinsic_02, self).__init__()
        self.group = 0
        return

#52 @all
class dataintrinsic_03(dataPosInt):
    def __init__(self):
        super(dataintrinsic_03, self).__init__()
        self.group = 0
        return

#53 @all
class dataintrinsic_04(dataPosInt):
    def __init__(self):
        super(dataintrinsic_04, self).__init__()
        self.group = 0
        return

#54 @all
class dataintrinsic_05(dataPosInt):
    def __init__(self):
        super(dataintrinsic_05, self).__init__()
        self.group = 0
        return

#55 @all
class dataintrinsic_06(dataPosInt):
    def __init__(self):
        super(dataintrinsic_06, self).__init__()
        self.group = 0
        return

#56 @all
class dataintrinsic_07(dataPosInt):
    def __init__(self):
        super(dataintrinsic_07, self).__init__()
        self.group = 0
        return

#57 @all
class dataintrinsic_08(dataPosInt):
    def __init__(self):
        super(dataintrinsic_08, self).__init__()
        self.group = 0
        return

#58 @all
class dataintrinsic_09(dataPosInt):
    def __init__(self):
        super(dataintrinsic_09, self).__init__()
        self.group = 0
        return

#59 @all
class dataintrinsic_10(dataPosInt):
    def __init__(self):
        super(dataintrinsic_10, self).__init__()
        self.group = 0
        return

#60 @all
class dataintrinsic_11(dataPosInt):
    def __init__(self):
        super(dataintrinsic_11, self).__init__()
        self.group = 0
        return

#61 @all
class dataintrinsic_12(dataPosInt):
    def __init__(self):
        super(dataintrinsic_12, self).__init__()
        self.group = 0
        return

#62 @all
class dataintrinsic_13(dataPosInt):
    def __init__(self):
        super(dataintrinsic_13, self).__init__()
        self.group = 0
        return

#63 @all
class dataintrinsic_14(dataPosInt):
    def __init__(self):
        super(dataintrinsic_14, self).__init__()
        self.group = 0
        return

#64 @all
class dataintrinsic_15(dataPosInt):
    def __init__(self):
        super(dataintrinsic_15, self).__init__()
        self.group = 0
        return

#65 @test3
class datakposition(dataChoice):
    def __init__(self):
        super(datakposition, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2}
        self.numOMap = {0: 'NA', 1: '1', 2: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 3

#66 @test3
class datakratio(dataCol):
    def __init__(self):
        super(datakratio, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'x': -1, '15-18': 17, 'oops': -1, '0.1': 1, 'Z': -1, '5.5': 6, '0.5': 1, '10:02': 2, '10:04': 4, 
                        '10:12': 12, '10:03': 3, '4, messed up on last 2 my b did the opposite': 4, '0.8': 1, '30?': 30, '1,000': 1000, 
                        'pp': -1, '45+66': 111, '3 times': 3, '2 times': 2, 'many': -1, 'severally': -1, 'twice': 2, 'three': 3, '4.6': 5, 
                        '6-Apr': -1, '5-Mar': -1, '8-Jun': -1, '8-Apr': -1, '0.2': 1, '0.3': 1, '0?': 0, "I'm not sure": -1, 
                        'I really dont kmow maybe 3': 3, "I don't know": -1, '1.5': 2, '6,4': -1, '8,2': -1, '7,3': -1, '3,7': -1, 'less than .5': 1, 
                        '?': -1, '1.8': 2, '1.4': 1, '1.1': 1, '0.7': 1, '0.75': 1}
        
        self.group = 3
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#67 @test5
class datalowpower(dataNaturalLanguage):
    def __init__(self):
        super(datalowpower, self).__init__()
        self.group = 11
        return

#68 @test3
class datalposition(dataChoice):
    def __init__(self):
        super(datalposition, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2}
        self.numOMap = {0: 'NA', 1: '1', 2: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 3
        return

#69 @test3
class datalratio(dataCol):
    def __init__(self):
        super(datalratio, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'x': -1, '15-18': 17, 'oops': -1, '0.1': 1, 'Z': -1, '5.5': 6, '0.5': 1, '10:02': 2, '10:04': 4, 
                        '10:12': 12, '10:03': 3, '4, messed up on last 2 my b did the opposite': 4, '0.8': 1, '30?': 30, '1,000': 1000, 
                        'pp': -1, '45+66': 111, '3 times': 3, '2 times': 2, 'many': -1, 'severally': -1, 'twice': 2, 'three': 3, '4.6': 5, 
                        '6-Apr': -1, '5-Mar': -1, '8-Jun': -1, '8-Apr': -1, '0.2': 1, '0.3': 1, '0?': 0, "I'm not sure": -1, 
                        'I really dont kmow maybe 3': 3, "I don't know": -1, '1.5': 2, '6,4': -1, '8,2': -1, '7,3': -1, '3,7': -1, 'less than .5': 1, 
                        '?': -1, '1.8': 2, '1.4': 1, '1.1': 1, '0.7': 1, '0.75': 1}
        
        self.group = 3
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#70 @all
class datamajor(dataChoice):
    def __init__(self):
        super(datamajor, self).__init__()
        #refer to https://www.ets.org/s/gre/pdf/dept_major_field_codes.pdf
        self.numIMap = {'na': 0, 'exercise science': 1, 'nursing': 1, 'psychology': 4, 'chemistry': 2, 'pre-med': 2, 'early childhood education': 6, 
                        'intervention specialist k-12': 6, 'biolgy': 1, 'integrated social studies': 4, 'athletic training': 1, 'integrated mathematics education': 6, 
                        'business management': 7, 'education- middle grades': 6, 'sports management': 7, 'psychology and religion': 4, 'dietetics': 1, 'undecided': 8, 
                        'environmental science, geology': 2, 'social work': 4, 'education': 6, 'finance': 7, 'criminal justice': 4, 'social work and psychology': 4, 
                        'toxicology': 1, 'english': 5, 'forensic biology': 1, 'marketing': 7, 'nusring': 1, 'business administration': 7, 'public relations': 8, 
                        'early childhood': 6, 'marketing and graphic design': 7, 'commercial art': 5, 'political science & public relations': 4, 'elementary/special ed.': 6, 
                        'business management and leadership': 7, 'electrical engineering': 3, 'cis': 2, 'biology': 1, 'sports communication and psychology': 4, 
                        'business management and leadership with a concentration in hr': 7, 'mechanical engineering': 3, 'health science': 1, 'hospitality leadership': 7, 
                        'undecided but leaning towards education': 6, 'civil engineering': 3, 'accounting': 7, 'manufacturing engineering technology': 3, 
                        'advertising, graphic design, spanish': 8, 'business marketing': 7, 'hospitality and leadership': 7, 'communications': 3, 'religion': 8, 
                        'sports communication': 8, 'psychology, general': 4, 'aep': 3, 'animation and visual effects': 5, 'elementary education': 6, 'entrepreneurship': 7, 
                        'physics': 2, 'computer science': 2, 'm e': 3, 'business': 7, 'computer information systems': 2, 'retail merchandising': 7, 'television arts': 4, 
                        'management information systems': 7, 'chemistry preprofessional (pre-pharmacy)': 2, 'community wellness': 8, 'undecided-aep': 3, 
                        'mechanical engineer': 3, 'health science, religious studies': 1, 'health science/ physical therapy': 1, 'bcom - marketing w/ co op': 7, 
                        'bahon.': 0, 'criminology': 4, 'neuroscience': 1, 'cognitive science': 4, 'criminology & criminal justice': 4, 'it': 2, 
                        'neuroscience & mental health': 4, 'linguistics': 5, 'criminology and criminal justice': 4, 'journalism': 8, 'biology, minor in chemistry': 1, 
                        'biology (ba)': 1, 'history': 5, 'philosophy': 5, 'english ba': 5, 'child studies': 4, 'communication studies': 8, 'neuroscience and mental health': 4, 
                        'political science: international relations': 4, 'undeclared major': 8, 'criminal justice and criminology': 4, 'commerce': 7, 'exploratory': 8, 
                        'applied psychology and imc': 4, 'physical therapy': 1, 'ot': 1, 'cinema & photography': 5, 'film and photography visual arts': 5, 'occupational therapy': 1, 
                        'applied psychology': 4, 'sports studies': 7, 'cinema and photograpghy': 5, 'psyhology': 4, 'cmd': 8, 'speech pathology': 1, 'clinical health studies/pt': 1, 
                        'public health': 1, 'television/radio': 8, 'acting': 8, 'therapeutic recreation': 1, 'integrated marketing communications': 7, 'biochemistry': 1, 'tv-r': 8, 
                        'undeclared': 8, 'business administration, but switching to accouting': 7, 'economics': 7, 'cinema and photography': 5, 'television and radio': 8, 
                        'pre-professional program': 8, 'environmental studies major, nutrition promotion minor': 1, 'math education': 6, 'film, photography, visual arts': 5, 
                        'zoology': 1, 'art education': 6, 'iternational studies': 4, 'psych': 4, 'bio/pre med': 1, 'kinesiology': 1, 'business economics': 7, 'nutrition': 1, 
                        'mathematics': 2, 'supply chain management': 7, 'psychology with a minor in neuroscience': 4, 'interactive media studies': 8, 
                        'biology and premedical studies': 1, 'sports leadership and management': 7, 'special education': 6, 'business isa': 7, 'university studies': 8, 
                        'business undecided': 7, 'sports medicine': 1, 'bioengineering': 3, 'political science': 4, 'finance, political science': 7, 
                        'strategic communication': 8, 'universal studies': 8, 'kiniesology': 1, 'art and pre med': 5, 'microbiology/ pre-medicine': 1, 
                        'strategic communications': 8, 'finance and math': 7, 'human biology': 1, 'biomedical laboratory diagnostics': 1, 'art ed and english': 6, 
                        'arts and humanities': 5, 'advertising': 7, 'pre-medical': 1, 'pre med': 1, 'public policy': 4, 'pyschology': 4, 'uud': 8, 'human resource management': 7, 
                        'biomedical laboratory science': 1, 'human development and family studies': 4, 'vet tech': 1, 'genomics and molecular genetics': 1, 
                        'pre- dental (undeclared major)': 1, 'human biology and spanish': 1, 'social science education': 6, 'microbiology': 1, 'ec': 7, 'media and information': 8, 
                        'professional writing': 4, 'human bio': 1, 'sociology, minor in bioethics': 4, 'molecular genetics and genomics': 1, 'animal science': 1, 
                        'lyman briggs human biology': 1, 'psychology & studio art': 4, 'actuarial science/economics double major': 2, 'physiology': 1, 
                        'criminal justice specialization design': 4, 'special education and learning disabilities': 6, 'criminal justice and psychology': 4, 
                        'hospitality business': 1, 'psy': 4, 'child development': 4, 'cognitive neuroscience': 4, 'human biology, pre-med': 1, 'no preference': 8, 
                        'bus': 7, 'international business': 7, 'biotechnology': 3, 'architecture': 8, 'pre-nursing': 1, 'film': 5, 'earth sciences': 2, 'chemical engineering': 3, 
                        'pre nursing': 1, 'pre medicine': 1, 'business, finance': 7, 'sociology': 4, 'engineering': 3, 'community  health': 1, 'wildlife management': 1, 
                        'cell biology and neuroscience': 1, 'food and nutrition': 1, 'premed': 1, 'cell biology': 1, 'pre-physical therapy': 1, 'buisiness marketing': 7, 
                        'community health': 1, 'chemical and biological engineering': 3, 'pre-veterinary': 1, 'health and human development': 1, 'sociology/criminology': 4, 
                        'psychology and kinesiology': 4, 'music technology': 5, 'exersize science': 1, 'psych and philanthropic business': 4, 'pre-comm': 7, 'pre-commerce': 7, 
                        'undecided: maybe statistics': 2, 'biology and music': 1, 'marine biology': 1, 'english/political science': 5, 'legal studies': 8, 'exercise and sport science': 1, 
                        'busines': 7, 'studio art/art administration': 5, 'theatre': 5, 'exercise and sports science': 1, 'pychology': 4, 'biology (pre-medicine)': 1, 
                        'theater and music': 5, 'biology (pre-med)': 1, 'medical sonography': 2, 'exceptional education': 6, 'bio': 1, 'deciding': 8, 'exercise & sports science': 1, 
                        'dance': 4, 'information technology': 2, 'environmental science': 2, 'pschology': 4, 'radiologic sciences and therapy': 1, 'psycology': 4, 'mls': 1, 'japanese': 5, 
                        'computer science & engineering': 2, 'computer science and engineering': 2, 'cse': 2, "if i knew i'd tell you": 0, 'bio-medical engineering': 3, 
                        'biomedical engineering/bio engineering': 3, 'business finance': 7, 'radiology': 2, 'buisness': 7, 'biology: pre-med': 1, 'pre-medicine': 1, 
                        'health and rehabilitation': 1, 'art, illustration / animation': 5, 'business administration and management': 7, 'sports industry': 7, 'neonatal nurse': 1, 
                        'sports nutrition': 1, 'psyhcology': 4, 'exercise science and nutrition': 1, 'bioloogy': 1, 'culinary arts': 5, 'business- human resources': 7, 
                        'business (marketing)': 7, 'business-marketing': 7, 'human nutrition': 1, 'mathematics education': 6, 'medical laboratory science': 1, 
                        'pharmaceutical sciences': 1, 'exploring': 8, 'undiceded': 8, 'dental hygiene': 1, 'medical lab science': 1, 'radiological sciences and therapy': 1, 
                        'hospital administration': 7, 'sports industries': 7, 'biological studies': 1, 'health sciences': 1, 'medical lab sciences': 1, 'speech-language pathology': 1, 
                        'athletic training too personal therapy': 1, 'hospitality managemnet': 7, 'industrial design': 5, 'pharmacy': 1, 'no idea yet.': 8, 
                        'business/accounting and finance': 7, 'kiniesiology': 1, 'chemistry or kinesiology or physics': 2, 'intended nursing': 1, 'kineseology': 1, 
                        'mathematics and art': 2, 'graphic design': 5, 'math': 2, 'psychology & english': 4, 'accouting': 7, 'undecided (possibly psychology)': 4, 
                        'intended psychology': 4, 'phd in psychology': 4, 'pssbs': 4, 'wildlife and fisheries science': 1, 'life science (pre-physical therapy)': 1, 
                        'life science': 1, 'business accountant': 7, 'psych and soc': 4, 'integrative arts': 5, 'business accounting': 7, 'pre-business': 7, 
                        'environmental engineering': 3, 'administration of justice': 8, 'kinesology': 1, 'psychological and social sciences': 4, 'corporate communications': 8, 
                        'non degree': 0, 'communications science and disorders': 1, 'psychology and social sciences': 4, 'broadcast journalism': 8, 'engineerin': 3, 
                        'letters, arts, and sciences': 5, 'psychological social sciences': 4, 'psyh': 4, 'integrative arts: music and psychology': 5, 
                        'psychological and social science b.a.': 4, 'pediatric nurse': 1, 'enineering': 3, 'none yet': 8, 'mechanical egineering': 3, 'communication': 2, 
                        'ist': 2, 'cj': 4, 'undecided- it': 2, 'psychology & social sciences': 4, 'science': 2, 'child and family development': 4, 'child & family develpoment': 4, 
                        'kinesiology with an emphasis in pre-physical therapy': 1, 'pre-child development': 4, 'biology bs': 1, 'journalism with an emphasis in media studies': 8, 
                        'speech, language, and hearing sciences': 8, 'biology with emphasis in cell and molecular biology': 1, 'health communication': 1, 'biology/ predental': 1, 
                        'communications and economics': 7, 'civil engineer': 3, 'foods and nutrition': 1, "i don't have one": 8, 'not applicable': 8, 'management': 7, 
                        'hospitality & tourism management hotels emphasis': 7, 'human resources management': 7, 'speech language and hearing sciences': 8, 'liberal studies': 5, 
                        'kinesiology-pre physical therapy': 1, 'business admin': 7, 'gerontology': 4, 'speech,language, and hearing sciences': 8, 'speech language pathology': 1, 
                        'computer engineering': 3, 'social work, minor in sociology': 4, 'general business': 7, 'kines- pre pt': 1, 'aerospace engineering': 3, 'allied health': 1, 
                        'theatre arts': 5, 'bims': 1, 'biomedical science': 1, 'general studies': 8, 'biol': 1, 'agbusiness': 1, 'bussniness administration': 7, 
                        'international relations': 4, 'nutritional sciences': 1, 'human resource development': 7, 'sport management': 7, 'engr': 3, 'ag leadeship and development': 7, 
                        'biomedical engineering': 3, 'unspecified business': 7, 'music': 5, 'kine': 1, 'business administration, accounting': 7, 'business honors': 7, 
                        'english (literature)': 5, 'international studies': 4, 'pre-med bep': 1, 'telecommunications and media studies': 2, 'ee': 3, 'agg': 0, 'exercise physiology': 1, 
                        'health': 1, 'bio medical science': 1, 'biochemistry and genetics': 1, 'kinesiology (aep)': 1, 'anthropology': 4, 'telecommunication': 2, "i don't know": 0, 
                        'biomedical sciences': 1, 'school health': 1, 'molecular and cell biology': 1, 'general engineering': 3, 'geophysics': 2, 'economy': 7, 'man econ': 7, 
                        'sociology and economics': 7, 'linguistic': 5, 'human development': 4, 'npb': 1, 'native american studies': 4, 'english/psychology': 5, 'economic': 7, 
                        'nutritional biology': 1, 'nutrition science': 1, 'biological science': 1, 'biological sciences': 1, 'design': 5, 'biochemistry and molecular biology': 1, 
                        'genetics': 1, 'neurology physiology and behavior': 4, 'music, psychology (mathematics emphasis)': 5, 'psychology and chinese': 5, 
                        'neurobiology, physiology and behavior': 5, 'psychology and communications': 5, 'nutrition sciences': 1, 'managerial economics': 7, 
                        'psychology and human development': 4, 'neurobiology, physiology, and behavior': 4, 'pscyhology': 4, 'neurobiology, physiology, behavior': 4, 
                        'psychology and economics': 4, 'cell biology but switching to managerical economics': 1, 'community and regional development': 4, 
                        'materials science and engineering': 2, 'undeclared life science': 1, 'political science and psychology': 4, 'natural science': 2, 'exercise bio': 1, 
                        'linguistics and human development': 4, 'pharmaceutical chemistry': 2, 'econ/admin': 7, 'undeclared - chass': 8, 'law and society/sociology': 4, 
                        'undecided in chass': 8, 'history/law and society': 4, 'pre-businees': 7, 'chass undeclared': 8, 'sociology law/soceity': 4, 'theater': 5, 
                        'undeclared chass': 8, 'business economic': 4, 'psych/bio (pre-med)': 4, 'global studies': 4, 'psychology and philosophy': 4, 
                        'asian studies (comparative track)': 4, 'bio-chemistry': 1, 'art': 5, 'pre business': 7, 'cultural anthropology': 4, 'economics/administrative studies': 7, 
                        'language': 5, 'statistics': 2, 'language and literature': 5, 'undelcared': 8, 'soc/ law and society': 4, 'undeclared-focus on psychology': 4, 
                        'french ba': 5, 'biological anthropology': 4, 'apk': 1, 'pre-public health': 1, 'behavioral and cognitive neuroscience': 2, 'health and human performance': 1, 
                        'applied physiology and kinesiology': 1, 'electrical/computer engineering': 3, 'human health and behavior': 1, 'anthropology/health science': 1, 
                        'exploratory humanities': 4, 'family, youth, and community sciences': 4, 'communication sciences and disorders': 1, 'wildlife conservation and management': 1, 
                        'tourism, recreation, and event management': 7, 'microbiology and cell science': 1, 'pre professional health sciences': 1, 'preprofessional': 8, 
                        'visual art studies and premed': 5, 'biology/anthropology': 1, 'health sciences pre-law': 1, 'psychology premed': 4, 'telecommunications': 2, 'event management': 7, 
                        'parks, recreation and tourism': 1, 'food science & human nutrition': 1, 'biology and history': 1, 'psychology and criminology': 4,
                        'computer/electrical engineering': 3, 'communication sciences & disorders': 1, 'health science, pre-physical therapy': 1, 'biology and health science': 1, 
                        'family, youth and community science': 4, 'general health sciences': 1, 'family youth and community sciences': 4, 'hospitality and tourism managemnet': 7, 
                        'health science - preprofessional': 1, 'dual degree education and sports coaching minor in child and family studies': 6, 'polymer science and engineering': 2, 
                        'ids': 8, 'psychology.': 4, 'education of the deaf': 6, 'recording industry production': 7, 'speech pathology and audiology': 1, 
                        'business administration management': 7, 'forensic science': 2, 'mass communications': 8, 'communications(bs)': 8, 'kinesiotherapy': 1, 
                        'life sciences': 1, 'computer science specialist': 2, 'public accounting': 7, 'life science first year': 1, 'i have not decided yet.': 8, 
                        'statistics and physics': 2, 'ecology and evolutionary biology, and biological anthropology': 1, 'mathmetics': 2, 'immunology and human biology': 1, 
                        'neuroscience specialist': 1, 'biochemistry and molecular genetics and microbiology': 1, 
                        'life science is my program, i choose a major at the end of first year. will probably choose physiology and something else': 1, 
                        'hummanities': 4, 'mathematics and economics': 2, 'actuarial science': 2, 'poli sci': 2, 'molecular genetics and microbiology': 1, 
                        'pharmacology specialist program': 1, 'rotman commerce': 7, 'animal physiology and neuroscience': 1, 'life science (psychology)': 1, 
                        'linguistics and spanish': 5, 'actuarial sciences': 2, 'computer sciences': 2, 'computer science, economics(minor)': 2, 'life sci- unsure major': 1, 
                        'history.': 5, 'molecular genetics': 1, 'planning to major in psychology': 4, 'immunology': 1, 'economics and finance math.': 7, 'pharmacology (?)': 1, 
                        'econ': 7, 'global health (undecided)': 1, 'mathematical application in finance and economics': 7, 
                        "i don't have one yet since i'm in first year but i'd like to major in nutrition science": 1, 'first year life science': 1, 'probably biology': 1, 
                        'computer science / music': 2, 'systems and information engineering': 3, 'biochemistry or nuerobiology': 1, 'chemistry with biochemistry specialization': 1, 
                        'computer science & pre-commerce': 2, 'undecided!': 8, 'cs/studio art': 2, 'n/a': 0, 'systems engineering': 3, 'global development studies': 4, 
                        'biology/spanish': 1, 'poetry writing': 5, 'chemistry or biology': 1, 'american govt': 4, 'mechanical or bme': 3, 'biology b.s.': 1, 'precomm': 8, 
                        'youth and social innovations': 4, 'environmental sciences': 1, 'spanish and music': 5, 'civil and environmental engineering': 3, 'engineering undecided': 3, 
                        'batten school of leadership and public policy': 7, 'media studies': 8, 'global health': 1, 'economics / foreign affairs': 7, 'foreign affairs': 7, 
                        'global commerce': 7, 'pre-med, undecided': 1, 'medicine': 1, 'mathematics, business': 2, 'college': 0, 'pre comm': 8, 'engr and econ': 3, 'drama': 5, 
                        'psychology/pre-med': 4, 'economics/spanish; pre-comm': 7, 'biochemistry, but i will change': 1, 'neuroscience (intended)': 1, 
                        'undecided, but probably either psychology or biology': 1, 'history and hopefully finance': 5, 'engineering, undecided': 3, 'linguistics and psychology': 4, 
                        'pre-dental': 1, 'art history': 5, 'french, pre-med': 5, 'information systems': 2, 'biology major': 1, 'biology pre-med': 1, 'pre-radiation science': 1, 
                        'undecided working toward egineering': 3, 'illustration': 8, 'undeclared (considering psychology)': 4, 'costume design bfa': 5, 'kinetic imaging': 1, 
                        'business marketing and mass communications (public relations)': 7, 'health sciences on a pre-nursing track': 1, 'bio (pre-med)': 1, 
                        'health, physical education & exercise science, concentration in health science': 1, 'psychology on a pre-radiation science track': 4, 
                        'chemical and life science engineering': 3, 'biology;pre-med': 1, 'music education': 6, 'hsep/ poli sci conc: intl relations': 4, 'bio track to nursing': 1, 
                        "i'm double majoring in criminal justice & homeland security & emergency preparedness.": 4, 'technical theatre: lighting design': 5, 'general science': 2, 'bio (pre-nursing)': 1}
        self.numOMap = {0: 'NA', 1: 'life sciences', 2: 'physical sciences', 3: 'engineering', 4: 'social and behavioral sciences', 5: 'humanities and arts', 6: 'education', 7: 'business', 8: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 9
        self.defaultNum = 0
        self.mapLowerCase = True

        self.group = 0
        return

#71 @test10
class datamcdv1(dataInt):
    def __init__(self):
        super(datamcdv1, self).__init__()
        self.minInt = -3
        self.invalid = 'NA'
        self.group = 10
        return

#72 @test10
class datamcdv2(dataInt):
    def __init__(self):
        super(datamcdv2, self).__init__()
        self.minInt = -3
        self.invalid = 'NA'
        self.group = 10
        return

#73 @test10
class datamcfiller1(dataPosInt):
    def __init__(self):
        super(datamcfiller1, self).__init__()
        self.group = 10
        return

#74 @test10
class datamcfiller2(dataPosInt):
    def __init__(self):
        super(datamcfiller2, self).__init__()
        self.group = 10
        return

#75 @test10
class datamcfiller3(dataPosInt):
    def __init__(self):
        super(datamcfiller3, self).__init__()
        self.group = 10
        return

#76 @test10
class datamcmost1(dataChoice):
    def __init__(self):
        super(datamcmost1, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#77 @test10
class datamcmost2(dataChoice):
    def __init__(self):
        super(datamcmost2, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#78 @test10
class datamcmost3(dataChoice):
    def __init__(self):
        super(datamcmost3, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#79 @test10
class datamcmost4(dataChoice):
    def __init__(self):
        super(datamcmost4, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#80 @test10
class datamcmost5(dataChoice):
    def __init__(self):
        super(datamcmost5, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#81 @test10
class datamcsome1(dataChoice):
    def __init__(self):
        super(datamcsome1, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#82 @test10
class datamcsome2(dataChoice):
    def __init__(self):
        super(datamcsome2, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#83 @test10
class datamcsome3(dataChoice):
    def __init__(self):
        super(datamcsome3, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#84 @test10
class datamcsome4(dataChoice):
    def __init__(self):
        super(datamcsome4, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#85 @test10
class datamcsome5(dataChoice):
    def __init__(self):
        super(datamcsome5, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, '1': 0, '2': 1}
        self.numOMap = {-1: 'NA', 0: '1', 1: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#86 @~test9
class datamood_01(dataChoice):
    def __init__(self):
        super(datamood_01, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

#87 @~test9
class datamood_02(dataChoice):
    def __init__(self):
        super(datamood_02, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

#88 @all
class datanfc_01(dataPosInt):
    def __init__(self):
        super(datanfc_01, self).__init__()
        self.group = 0
        return

#89 @all
class datanfc_02(dataPosInt):
    def __init__(self):
        super(datanfc_02, self).__init__()
        self.group = 0
        return

#90 @all
class datanfc_03(dataPosInt):
    def __init__(self):
        super(datanfc_03, self).__init__()
        self.group = 0
        return

#91 @all
class datanfc_04(dataPosInt):
    def __init__(self):
        super(datanfc_04, self).__init__()
        self.group = 0
        return

#92 @all
class datanfc_05(dataPosInt):
    def __init__(self):
        super(datanfc_05, self).__init__()
        self.group = 0
        return

#93 @all
class datanfc_06(dataPosInt):
    def __init__(self):
        super(datanfc_06, self).__init__()
        self.group = 0
        return

#94 @test3
class datanposition(dataChoice):
    def __init__(self):
        super(datanposition, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2}
        self.numOMap = {0: 'NA', 1: '1', 2: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 3
        return

#95 @test3
class datanratio(dataCol):
    def __init__(self):
        super(datanratio, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'x': -1, '15-18': 17, 'oops': -1, '0.1': 1, 'Z': -1, '5.5': 6, '0.5': 1, '10:02': 2, '10:04': 4, 
                        '10:12': 12, '10:03': 3, '4, messed up on last 2 my b did the opposite': 4, '0.8': 1, '30?': 30, '1,000': 1000, 
                        'pp': -1, '45+66': 111, '3 times': 3, '2 times': 2, 'many': -1, 'severally': -1, 'twice': 2, 'three': 3, '4.6': 5, 
                        '6-Apr': -1, '5-Mar': -1, '8-Jun': -1, '8-Apr': -1, '0.2': 1, '0.3': 1, '0?': 0, "I'm not sure": -1, 
                        'I really dont kmow maybe 3': 3, "I don't know": -1, '1.5': 2, '6,4': -1, '8,2': -1, '7,3': -1, '3,7': -1, 'less than .5': 1, 
                        '?': -1, '1.8': 2, '1.4': 1, '1.1': 1, '0.7': 1, '0.75': 1}
        self.group = 0
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#96 @all
class datapate_01(dataPosInt):
    def __init__(self):
        super(datapate_01, self).__init__()
        self.group = 0
        return

#97 @all
class datapate_02(dataPosInt):
    def __init__(self):
        super(datapate_02, self).__init__()
        self.group = 0
        return

#98 @all
class datapate_03(dataChoice):
    def __init__(self):
        super(datapate_03, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

#99 @all
class datapate_04(dataChoice):
    def __init__(self):
        super(datapate_04, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

#100 @all
class datapate_05(dataChoice):
    def __init__(self):
        super(datapate_05, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

#101 @test3
class datarposition(dataChoice):
    def __init__(self):
        super(datarposition, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2}
        self.numOMap = {0: 'NA', 1: '1', 2: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 3
        return

#102 @test3
class datarratio(dataCol):
    def __init__(self):
        super(datarratio, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'x': -1, '15-18': 17, 'oops': -1, '0.1': 1, 'Z': -1, '5.5': 6, '0.5': 1, '10:02': 2, '10:04': 4, 
                        '10:12': 12, '10:03': 3, '4, messed up on last 2 my b did the opposite': 4, '0.8': 1, '30?': 30, '1,000': 1000, 
                        'pp': -1, '45+66': 111, '3 times': 3, '2 times': 2, 'many': -1, 'severally': -1, 'twice': 2, 'three': 3, '4.6': 5, 
                        '6-Apr': -1, '5-Mar': -1, '8-Jun': -1, '8-Apr': -1, '0.2': 1, '0.3': 1, '0?': 0, "I'm not sure": -1, 
                        'I really dont kmow maybe 3': 3, "I don't know": -1, '1.5': 2, '6,4': -1, '8,2': -1, '7,3': -1, '3,7': -1, 'less than .5': 1, 
                        '?': -1, '1.8': 2, '1.4': 1, '1.1': 1, '0.7': 1, '0.75': 1}
        self.group = 3
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#103 @test5
class datasarcasm(dataPosInt):
    def __init__(self):
        super(datasarcasm, self).__init__()
        self.group = 5
        return

#104 @test9
class dataselfesteem_01(dataPosInt):
    def __init__(self):
        super(dataselfesteem_01, self).__init__()
        self.group = 9
        return

#105 @~test9
class datastress_01(dataPosInt):
    def __init__(self):
        super(datastress_01, self).__init__()
        self.group = 0
        return

#106 @~test9
class datastress_02(dataPosInt):
    def __init__(self):
        super(datastress_02, self).__init__()
        self.group = 0
        return

#107 @~test9
class datastress_03(dataPosInt):
    def __init__(self):
        super(datastress_03, self).__init__()
        self.group = 0
        return

#108 @~test9
class datastress_04(dataPosInt):
    def __init__(self):
        super(datastress_04, self).__init__()
        self.group = 0
        return

#109 @test7
class datatempest1(dataCol):
    def __init__(self):
        super(datatempest1, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'room temperature': -1, '75': 75, '72 degrees F': 72, '70': 70, '25 degrees': 77, '76': 76, '78': 78,
                        '45': -1, '65': 65, '72': 72, '68': 68, '74': 74, '60': 60, '75 degrees': 75, '70 degrees': 70, '69': 69, '69-70 degrees': 70,
                        '73': 73, '68F': 68, '63': 63, '67': 67, '70 degrees F': 70, '50': -1, '66': 66, '72 degrees': 72, '60-65': 63, '80': 80, '82': 82,
                        'I do not know': -1, '76 degrees fahrenheit': 76, '61': 61, '64 degrees': 64, '34': 93, '68 degrees Fahrenheit': 68, '71': 71,
                        '65 degrees': 65, '55': 55, 'room temp': -1, '67 degrees': 67, '70ish': 70, '79': 79, 'room temp.': -1, '~70 degrees': 70,
                        'comfortable, ~73deg': 73, '70 degrees fahrenheit': 70, '~75 degrees': 75, '62': 62, '64': 64, '59': 59, '69.8': 70, '66.2': 66,
                        '62.6': 63, '53.6': 54, '46.4': -1, '77': 77, '64.4': 64, '35.6': -1, '57.2': -1, '71.6': 72, '78.8': 79, '80.6': 81, '39.2': -1,
                        '58': -1, 'Unknown': -1, '~70': 70, 'no idea': -1, '40': -1, 'maybe 67': 67, '150': -1, '65 degrees F': 65, '68 degrees': 68,
                        'normal? like 68?': 68, 'room': -1, '85': 85, '70-ish': 70, 'about 72 degrees': 72, 'about 70': 70, '70?': 70, '55f': 55,
                        '298': -1, '98.6': 99, '70*F': 70, '72 F': 72, '70 F': 70, '68 Degrees': 68, 'between 65-75': 70, '65-70': 68, '68.3': 68,
                        '73 F': 73, '75-85': 80, '75.2': 75, 'Room Temperture': -1, '32': 89, '78F': 78, '54': -1, '70-75': 73, '20': 68, '35': 95,
                        "In the mid to upper 70's": 78, 'around 65-70 degrees': 68, '97': 97, '72.3': 72, '60-70': 65,
                        'Chilly. I have no idea what the exact  temperature is.': -1, '57': 57, 'normal': -1, '22F': -1, '56': 56, '86': 86,
                        'somewhere between 68 and 72': 70, 'Very warm': -1, 'idk': -1, 'i dont know': -1, '98': 98, '89': 89, '39': 102,
                        'Room Temperature': -1, '90': 90, 'cool': -1, 'Hot': -1, 'yes': -1, 'good': -1, '81': 81, '78 degrees': 78, '88': 88, '100': 100,
                        '73 degrees': 73, '30': 86, '80 degrees Fahrenheit': 80, '38': 100, 'May be about 70': 70, '~72': 72, 'room temp. 71': 71, '28': 82,
                        '~74': 74, '80 Fahrenheit': 80, '72F': 72, "I don't know": -1, '75F': 75, '74 degrees': 74, 'Room temperature': -1,
                        '80 degrees': 80, "I'm not sure": -1, '84': 84, '73 degrees F': 73, '70F': 70, '73.4': 73, '424.4': -1, '25': 77, 'Warm': -1,
                        'about 75 degrees': 75, '83': 83, '87': 87, 'warm, maybe 70 degrees Fahrenheit': 70, 'the temperature feels around 78 fahrenheit': 78,
                        '60 degrees?': 60, 'THE ENVIRONMENT IS PRETTY WARM, AND STABLE.': -1, 'no idea, slightly cool though': -1}

        self.group = 7
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            iData = int(iData)
            if iData > 100: #[100, inf]
                return -1
            elif iData <= 40:
                if iData < 15: #[-inf, 15]
                    return -1
                else: #[15, 40]
                    return int(iData * 1.8) + 32
            elif iData < 55: #[40, 55]
                return -1
            else: #[55, 100]
                return iData
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#110 @test7
class datatempest2(dataPosInt):
    def __init__(self):
        super(datatempest2, self).__init__()
        self.group = 7
        return

#111 @test7
class datatempest3(dataPosInt):
    def __init__(self):
        super(datatempest3, self).__init__()
        self.group = 7
        return

#112 @test7
class datatempfollowup1(dataPosInt):
    def __init__(self):
        super(datatempfollowup1, self).__init__()
        self.group = 7
        return

#113 @test7
class datatempfollowup2(dataPosInt):
    def __init__(self):
        super(datatempfollowup2, self).__init__()
        self.group = 7
        return

#114 @test7
class datatempfollowup3(dataPosInt):
    def __init__(self):
        super(datatempfollowup3, self).__init__()
        self.group = 7
        return

#115 @test3
class datavposition(dataChoice):
    def __init__(self):
        super(datavposition, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2}
        self.numOMap = {0: 'NA', 1: '1', 2: '2'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 3
        return

#116 @test3
class datavratio(dataCol):
    def __init__(self):
        super(datavratio, self).__init__()
        self.type = 'str / int / int'
        self.numIMap = {'NA': -1, 'x': -1, '15-18': 17, 'oops': -1, '0.1': 1, 'Z': -1, '5.5': 6, '0.5': 1, '10:02': 2, '10:04': 4, 
                        '10:12': 12, '10:03': 3, '4, messed up on last 2 my b did the opposite': 4, '0.8': 1, '30?': 30, '1,000': 1000, 
                        'pp': -1, '45+66': 111, '3 times': 3, '2 times': 2, 'many': -1, 'severally': -1, 'twice': 2, 'three': 3, '4.6': 5, 
                        '6-Apr': -1, '5-Mar': -1, '8-Jun': -1, '8-Apr': -1, '0.2': 1, '0.3': 1, '0?': 0, "I'm not sure": -1, 
                        'I really dont kmow maybe 3': 3, "I don't know": -1, '1.5': 2, '6,4': -1, '8,2': -1, '7,3': -1, '3,7': -1, 'less than .5': 1, 
                        '?': -1, '1.8': 2, '1.4': 1, '1.1': 1, '0.7': 1, '0.75': 1}
        self.group = 3
        self.real = True
        return

    def numFore(self, iData):
        if iData.isdigit():
            return int(iData)
        elif iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#117 @test9
class dataworstgrade1(dataCol):
    def __init__(self):
        super(dataworstgrade1, self).__init__()
        self.type = 'str / (int, int) / (int, int)'
        #refer to stanford
        self.numIMap = {'NA': (-1, -1), 'Spring 2014': (2014, 6), '14-May': (2014, 5), 'spring 2014': (2014, 6), 'spring 2013': (2014, 6), 'Winter 2008': (2008, 3), 'Fall 2013': (2013, 12),
                        'Winter 2014': (2014, 3), 'Senior in High School': (-1, -1), 'Spring 2013': (2013, 6), 'Sping 2014': (2014, 3), 'Spring 2012': (2012, 6), 'Winter 2013': (2013, 3),
                        'Fall 2014': (2014, 12), 'High school senior': (-1, -1), 'Summer 2014': (2014, 8), 'fall 2014': (2014, 12), 'spring 2005': (2005, 6), 'winter 2013': (2013, 3),
                        'Before starting at Bradley, Spring 2014': (2014, 6), 'summer of 2014': (2014, 8), '14-Jun': (2014, 6), 'summer 2014': (2014, 8), 'winter 3013': (2013, 3),
                        'summer 2013': (2013, 8), 'winter 2014': (2014, 3), 'spring 14': (2014, 6), 'Prior to the current term? Spring 2014': (2014, 6), 'fall 2010': (2010, 12),
                        'NA (First term)': (-1, -1), 'highschool 2014': (-1, -1), 'Summer, 2014': (2014, 8), 'Summer 2013': (2013, 8), 'Winter 2012': (2012, 3),
                        'Winter and Fall 2014 (present)': (2014, 3), 'fall 2011': (2011, 12), 'winter2014': (2014, 3), 'winter 2014 (high school)': (2014, 3),
                        'June 2014 (High School)': (2014, 6), 'summer 4014': (2014, 8), 'Current - so last term was Spring 2014': (2014, 6),
                        "Spring 2014 (if you don't count the current term)": (2014, 6), 'spring of 2014': (2014, 6), 'high school 21014': (-1, -1), 'Spring 2014.': (2014, 6),
                        'Fall, 2014': (2014, 12), 'Currently still in school. Last full term was High School Fall of 2013-Spring 2014.': (2014, 6),
                        'sping 2014': (2014, 3), 'Fall 2017': (-1, -1), 'Spring 2015': (-1, -1), 'Now: Fall 2014': (2014, 12), 'Now (Fall 2014)': (2014, 12),
                        'currently in school so, Fall 2014': (2014, 12), "Fall '14": (2014, 12), 'currently': (-1, -1), '(High School) Spring 2014': (2014, 6), 'Fall 2015': (-1, -1),
                        'currently in school, last completed term Spring 2014': (2014, 6), 'Spring  2013': (2013, 6), 'spring2014': (2014, 6),
                        'This is my first semester at MSU. So my last term would my senior year of high school': (-1, -1),
                        'currently in school (Fall 2014)': (2014, 12), 'Spring2014': (2014, 6), 'Summer 2014#': (2014, 8), 'WINTER2012': (2012, 3), 'High school Spring 2014': (2014, 6),
                        'Spring 14': (2014, 6), 'Winter 2011': (2011, 3), 'spring 2011': (2011, 6), 'fall 2013': (2013, 12), 'Senior year - final semester': (-1, -1), 'spring 2010': (2010, 6),
                        '2014': (-1, -1), 'sophmore': (-1, -1), 'winter 2007': (2007, 3), 'Spring 2011': (2011, 6), 'FALL 2014': (2014, 12), 'fall 2008': (2008, 12), 'Spring 2014 (High School)': (2014, 6),
                        'SPRING 2014': (2014, 6), 'Fa;; 2-14': (2014, 12), 'winter2013': (2013, 3), 'winter 2008': (2008, 3), 'High school': (-1, -1), 'summer2014': (2014, 8), '13-May': (2013, 5),
                        'winter 2103': (2013, 3), 'current': (-1, -1), 'Fall 2014 (freshman)': (2014, 12), 'I am currently in school.': (-1, -1), 'fall2012': (2012, 12),
                        'Fall 2014(current)': (2014, 12), '5': (-1, -1), 'this is my first semester i graduated high school in 2012': (-1, -1), 'Autumn 2014': (2014, 12),
                        'Autum 2014': (2014, 12), 'currently in school. autum 2014': (2014, 12), 'autumn 2014': (2014, 12), 'Currently': (-1, -1), 'spring 2104': (2014, 6),
                        'high school': (-1, -1), 'This year:Winter 2014. Before that, Summer 2010': (2014, 3), 'High School 2012': (-1, -1),
                        'winter 2013, high school, i am a freshman at Newark': (2013, 3), 'Autum 14': (2014, 12), 'this is my first term': (-1, -1),
                        'spring 2014 for high school': (2014, 6), '14-Aug': (2014, 8), 'n/a': (-1, -1), '20 minutes ago.': (-1, -1), 'AUTUMN 2014': (2014, 12), '2013': (-1, -1),
                        'i was still in high school': (-1, -1), 'fall': (-1, -1), "I finished high school in June of 2014, so I haven't completed a whole term yet.": (-1, -1),
                        'Autumn 13': (2013, 12), 'now...': (-1, -1), 'may,spring 2014': (2014, 5), '26 hours ago': (-1, -1), 'WINTER 2014': (2014, 5), '14-Sep': (2014, 9), 'fall 20143': (-1, -1),
                        'Spring 2014 and currently': (2014, 6), 'High School so N/A?': (-1, -1), "I'm in school right now..": (-1, -1), 'spirng 2014': (2014, 6),
                        'Spring Semester 2014': (2014, 6), '(Spring 2014)': (2014, 6), 'Spring 2014 (High school)': (2014, 6), 'Spring 2014 (Currently in Fall 2014)': (2014, 6),
                        'Fall': (-1, -1), 'Spring': (-1, -1), '2010': (-1, -1), 'Spring 2014 (not including this term)': (2014, 6), 'spring 1997': (-1, -1), 'Fall 14': (2014, 12),
                        'Spring 204': (2014, 6), 'FAll 2014': (2014, 12), 'high school 2012': (-1, -1), 'high school 2014': (-1, -1), 'LAST SEMESTER': (-1, -1), '12th Grade': (-1, -1),
                        'sping2013': (2013, 3), 'Summer of 2013': (2013, 8), 'sep. 2013- jun. 2014': (2014, 6), 'Summer 2012': (2012, 8), 'spin 2014': (2014, 6), 'Summer 1 & 2 2014': (2014, 8),
                        'Spring 2001': (-1, -1), 'spring 201': (-1, -1), 'Summer & Fall 2014': (2014, 12), 'spring 2014 (high school)': (2014, 6), 'Fall2014': (2014, 12), 'Winter 1998': (-1, -1),
                        'FAll 2011': (2011, 12), 'Fall 2014 (Currently in school)': (2014, 12), 'Winter 2009': (2009, 3), 'The last term I was in school was the Spring of 2014': (2014, 6),
                        '13-Mar': (2013, 3), 'High School, Spring 2014': (2014, 6), 'Currently enrolled': (-1, -1), 'sPRING 2014': (2014, 6), 'winter 2013 - high school': (2013, 3),
                        'FALL2014': (2014, 12), 'This term, Fall 2014': (2014, 12), 'SPRING  2014': (2014, 6), 'Spring 201A': (-1, -1), 'Currently in school': (-1, -1),
                        'Spring 2013, last year - high school': (2013, 6), 'Summer Session 2 2014': (2014, 8), 'High School': (-1, -1), 'summer 2018': (-1, -1),
                        'spring 2015': (-1, -1), '2014 summer': (2014, 8), 'Summer Session II 2014': (2014, 8), 'Summer Session 1': (2014, 8), 'high school spring semester 2014': (2014, 6),
                        'Summer session 2 2014': (2014, 8), '2013 Fall': (2013, 12), 'Second Semester (High School, Senior Year)': (-1, -1), 'Summer Session 1 2014': (2014, 8),
                        'Summer session II': (-1, -1), 'SUMMER 2014': (2014, 8), 'Summer Session 2': (-1, -1), 'summer 14': (2014, 8), 'Summer2014': (2014, 8), 'summer': (-1, -1),
                        'Spring Quarter 2014': (2014, 6), 'Semester 2 2014': (2014, 6), 'Spring 2104': (2014, 6), 'fall 2014 is my first term': (2014, 12), 'SPRING 20114': (2014, 6),
                        "This is my first quarter. I'm a freshman": (-1, -1), 'Fall 2012': (2012, 12), 'This is my first term. Fall 2014.': (2014, 12), 'Summer B 2014': (2014, 8),
                        "I'm a freshman now so Highschool spring 2014": (2014, 6), "spring'14": (2014, 6), 'WINTER 2013': (2013, 3), 'Spring 2014 (Last Semester of High school)': (2014, 6),
                        'Fall 2010': (2010, 12), '41760': (-1, -1), '(spring14)': (2014, 6), 'spring': (-1, -1), 'spring 2012': (2012, 6), 'High school 2013-2014': (-1, -1), 'winter 2012': (2012, 3),
                        'Winter/Spring 2014': (2014, 6), 'Spring/Summer 2014 in Highschool': (2014, 8), 'February-July 2014': (2014, 7), '41852': (-1, -1), 'high school, June 2014': (2014, 6),
                        'Spring/Summer 2014': (2014, 8), "If you don't count now - fall 2014, then spring 2014.": (2014, 6), 'Winter 2013 (High School)': (2013, 3),
                        'Not counting this current semester, Spring 2014': (2014, 6), 'currently in school': (-1, -1), 'Currently in school.': (-1, -1),
                        'senior year of high school': (-1, -1), 'Spring 2014-present': (2014, 12), 'not counting this term, Spring 2013': (2013, 6),
                        'Fall 2014 (First year student)': (2014, 12), 'Srping 2014': (2014, 6), 'Winter 2013-2014': (2014, 3), '2013-2014 highschool': (-1, -1),
                        'Fall, 2014 (still in session), if this means last full term: Spring, 2014': (2014, 6), 'sring 2014': (2014, 6),
                        'winter of 2014 in high school': (2014, 3), 'Spring/Summer 2013': (2013, 8), '1 hour ago': (-1, -1), 'Fall 2013?': (2013, 12), 'an hour ago': (-1, -1)}
        self.group = 9
        self.real = True
        return

    def numFore(self, iData):
        if iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return (-1, -1)

    def numBack(self, oData):
        if oData == (-1, -1):
            return 'NA'
        else:
            return '%d %d' %(oData[1], oData[0])

    def codeFore(self, iData):
        if iData == (-1, -1):
            return (self.real, False, (0, 0))
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return iData
        else:
            return (-1, -1)

#118 ~@test9
class dataworstgrade2(dataCol):
    def __init__(self):
        super(dataworstgrade2, self).__init__()
        self.type = 'str / int / int'
        #refer to https://www.rapidtables.com/calc/grade/gpa-to-letter-grade-calculator.html
        self.numIMap = {'na': -1, 'a - 97%': 97, 'c': 76, 'c-': 72, 'b': 86, 'a': 96, '94': 94, 'a+': 100, '98': 98, 'b+': 89, '99%': 99, 'c+': 79, '98%': 98, 'gpa was a 3.2': 89, 'b-': 82,
                        'a plus': 100, '100%': 100, '88%': 88, 'psychology': -1, 'a-': 92, '93': 93, '87% b': 87, 'physics': -1, '92%': 92, 'pre-calculus, with a low d': 66, 'f': 59,
                        '83': 83,'math': -1, '90%': 90, 'd': 66, '80': 80, '82%': 82, '100': 100, '86': 86, '90': 90, '91%': 91, '103%': 103, '67%': 67, '75': 75, 'withdrawn': -1, '72%': 72,
                        'na (first term)': -1, '88': 88, '60%': 60, '78': 78, '92': 92, '91': 91, '68': 68, '89%': 89, '85': 85, 'competent (c)': 73, '78%': 78, '60': 60, '79%': 79,
                        '70%': 70, '70': 70, '107': 107, '75%': 75, '89': 89, '104': 104, '3.5': 92, '74': 74, '84': 84, '81': 81, '96': 96, '103': 103, '97%': 97, '76': 76, '95%': 95, '3.33': 89,
                        'for spring 2014: 98%': 98, '105%': 105, 'chemistry- 88%': 88, '97': 97, '2': 76, '77%': 77, '74%': 74, '80%': 80, '2.5': 82, '4': 96, '4.0-a': 96, '1.5': 72,
                        'i have not received grades yet for fall 2014 but in the past the worst grade i had gotten would have been a b+.': 89, 'cse iss mth stt  3.0': 86,
                        'e': 59, '69%': 69, 'general business b+': 89, '79': 79, '3': 86, '86%': 86, '3.5 (85%)': 85, 'gpa 3.5': 92, '85%': 85, '96%': 96, '4.0- a': 96, '94%': 94,
                        '112.98%': 113, 'a (95%)': 95, '93%': 93, '71%': 71, '0': 59, 'withdraw': -1, 'b+ 88%': 88, 'chemistry,90': 90, '#name?': -1, '83%': 83, '87': 87, '76%': 76, '101.5': 102,
                        '95': 95, '57%': 57, 'high school (a+)': 100, '82': 82, 'd-': 62, '66%': 66, '99': 99, '2.8': 86, 'like a 85': 85, '90% english': 90,
                        'had to pass/fail a math course, 61%': 61, 'c mabye?': 76, 'government': -1, 'my best final grade was a 100%': 100, '3.3': 89, "a's": 96, 'n/a': -1,
                        '108%': 108, 'freshman': -1, 'b, in ap english.': 86, '90 percent': 90, '58%': 58, 'c 78%': 78, 'w': -1,
                        'the best grade i got last year my senior year was an a': 96, '72': 72, 'educational psychology': -1, 'freshman this semester': -1, 'english 97': 97,
                        '73': 73, 'my best final grade was an 92% in psychology': 92, "as'": 96, 'summer: a': 96, '84%': 84, 'i believe it was a 64': 64, '65%': 65, '1': 66,
                        '65': 65, 'my best final grade was an a-': 92, 'a-97%': 97, '+c': 79, 'history': -1, 'high scool 97%': 97, 'a-92': 92,
                        'still on my first semester, but so far chemistry': -1, 'havent yet': -1, 'med micro': -1, '0.83': 83, '89.9': 90, '0.32': 32, 'd+': 69, '3.9': 96, '0.91': 91,
                        '0.75': 75, '0.98': 98, '0.76': 76, '0.82': 82, '0.95': 95, '0.79': 79, '0.88': 88, '0.86': 86, '0.9': 90, '0.56': 56, '~90%': 90, '0.85': 85,
                        'my best grade was an 89%.': 89, 'a (94%)': 94, '0.5': 50, '0.87': 87, 'n/a in high school, b.': 86, 'c 70%': 70, '0.94': 94, '0.65': 65, 'b +': 89, '0.7': 70,
                        '3.83': 96, '0.93': 93, 'a- to b+': 89, '0.99': 99, '100% a': 100, "n/a i'm an incoming freshman": -1, '85 b': 85, '3.2': 89, '0.798': 80, '105': 105, '0.6': 60,
                        '66': 66, '0.92': 92, '0.68': 68, '0.89': 89, '77': 77, '0.8': 80, '0.96': 96, '49': 49, '67': 67, '42104': -1, '0.45': 45, '0.23': 23, '63': 63, '0.78': 78, '0.77': 77,
                        'this is my first semester': -1, '90% in ap statiscs': 90, '87%': 87, 'economics a-': 92, 'politics of the middle east': -1, 'n/a (first year student)': -1,
                        '0.905': 91, '0.97': 97, '1.02': 102, 'got an a on my voice jury.': 96}
        
        self.group = 9
        self.real = True
        return

    def numFore(self, iData):
        iData = iData.lower()
        if iData in self.numIMap:
            return self.numIMap[iData]
        else:
            return -1

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, 0)
        else:
            return (self.real, True, iData)

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return data
        else:
            return -1

#119 @test9
class dataworstgrade3(dataPosInt):
    def __init__(self):
        super(dataworstgrade3, self).__init__()
        self.group = 9
        return

#120 @test9
class dataworstgrade4(dataPosInt):
    def __init__(self):
        super(dataworstgrade4, self).__init__()
        self.group = 9
        return

#121 @test9
class dataworstgrade5(dataPosInt):
    def __init__(self):
        super(dataworstgrade5, self).__init__()
        self.group = 9
        return

#122 @all
class datayear(dataChoice):
    def __init__(self):
        super(datayear, self).__init__()
        #TODO: a better classification
        self.numIMap = {'na': 0, '2': 2, '1': 1, '3': 3, '4': 4, 'fifth year senior': 5, 'junior by credits': 3, 'fifth-year': 5,
                        'working on second bachelors degree': 6, 'post-bac': 6, 'sophmore credit wise but first year': 1, 'post bacc': 6,
                        'transfer': 6, '7': 6, 'senior year of highschool': 6, 'second/3rd': 2, 'with junior standing (running start)': 3,
                        'first year, but because of foreign credits from high-school, it counts at second year.': 1,
                        'has credits of junior': 3, 'professor': 6, 'continuing studies': 6, 'senior 5th year': 5, 'super senior 5+': 5,
                        'open university, post-bacc': 6, 'not applicable': 0, 'ali': 0, '6th year': 5, 'fifth year': 5, 'sixth year': 5,
                        '5th year': 5, 'transferred here this year': 6, '4th,but transfer': 4, 'super senior (fifth-year)': 5,
                        'with junior credits': 3, 'senior (fifth-year)': 5, 'transfer student; 4th year in college': 4, 'seniuor fifth year': 5,
                        '5th, after 16 month work term': 5, 'second degree': 6, '5th (but on exchange)': 5}
        self.numOMap = {0: 'NA', 1: 'first', 2: 'second', 3: 'third', 4: 'forth', 5: 'fifth or more', 6: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 7
        self.defaultNum = 0
        self.mapLowerCase = True
        self.group = 0
        return

#123 @all
class dataStation(dataNaturalLanguage):
    def __init__(self):
        super(dataStation, self).__init__()
        self.group = 11
        return

#124 @all #moved to #222 and #224
class dataDate_x(dataNaturalLanguage):
    def __init__(self):
        super(dataDate_x, self).__init__()
        self.group = 11
        return

#125 @all
class dataExperimenter(dataNaturalLanguage):
    def __init__(self):
        super(dataExperimenter, self).__init__()
        self.group = 11
        return

#126 @test7
class dataTemperatureinlab(dataPosInt):
    def __init__(self):
        super(dataTemperatureinlab, self).__init__()
        self.group = 7
        return

    def numFore(self, iData):
        if iData == 'N/A' or iData == 'NA':
            return -1
        else:
            iData = float(iData)
            if iData > 35:
                return int(iData)
            else:
                return int(iData * 1.8 + 32)

    def numBack(self, oData):
        if oData == -1:
            return 'N/A'
        else:
            return str(oData)

#127 @test2 test6
class dataOrderofTasks(dataChoice):
    def __init__(self):
        super(dataOrderofTasks, self).__init__()
        self.numIMap = {'II-SR': 1, 'SR-II': 2, 'NA': 0, 'II, SR': 1, 'SR, II': 2}
        self.numOMap = {0: 'NA', 1: 'II-SR', 2: 'SR-II'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 3
        self.group = 0
        return

#128 @test6
class dataClipboardWeight(dataChoice):
    def __init__(self):
        super(dataClipboardWeight, self).__init__()
        self.numIMap = {'20': 2, '10': 1, 'NA': 0}
        self.numOMap = {0: 'NA', 1: '10', 2: '20'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 3
        self.group = 6
        return

#129 @test6
class dataIIResponse(dataPosInt):
    def __init__(self):
        super(dataIIResponse, self).__init__()
        self.group = 6
        return

#130 @test2
class dataSRCondition(dataChoice):
    def __init__(self):
        super(dataSRCondition, self).__init__()
        self.numIMap = {'B': 2, 'C': 3, 'A': 1, 'NA': 0, 'b': 2, 'c': 3, 'a': 1, ' b': 2, '': 0}
        self.numOMap = {0: 'NA', 1: 'A', 2: 'B', 3: 'C'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 4
        self.group = 2
        return

#131 @test2
class dataSRMeetingResponse(dataChoice):
    def __init__(self):
        super(dataSRMeetingResponse, self).__init__()
        self.numIMap = {'Friday': 1, 'Monday': 2, 'Sunday': 3, 'P Skipped this page': 0, 'NA': 0, 'mon': 2, 'saturday': 3, 'Wednesday': 3,
                        'Thursday': 3, 'Saturday': 3,'Tuesday': 3, 'N/A': 0, 'monday': 2, 'Firday': 1, 'Monday ': 2, '': 0}
        self.numOMap = {0: 'NA', 1: 'Friday', 2: 'Monday', 3: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 4
        self.group = 2
        return

#132 @test2
class dataSRConfidenceResponse(dataPosInt):
    def __init__(self):
        super(dataSRConfidenceResponse, self).__init__()
        self.numIMap = {'5': 5, '4': 4, '3': 3, '2': 2, '1': 1, '...': -1, 'NA': -1, 'N/A': -1, '4.5': 4}
        self.group = 2
        return

    def numFore(self, iData):
        return self.numIMap[iData]

#133 @test2
class dataSRTFCorrect(dataPosInt):
    def __init__(self):
        super(dataSRTFCorrect, self).__init__()
        self.numIMap = {'Yes': 0, 'N/A': -1, 'No (4 Missed)': 4, 'No (3 missed)': 3, 'No (1 missed)': 1, 'No (2 missed)': 2,
                        'NA': -1, 'n/a': -1, 'No [1]': 1, 'No(3)': 3, 'No(1)': 1, 'No(4)': 4, 'No (2)': 2, 'No (1)': 1, 'No (4)': 4,
                        'N/a': -1, 'No (missed 2)': 2, 'No (missed 1)': 1, 'No (missed 3)': 3, 'No (missed No (missed 3))': 3,
                        'No (missed 4)': 4, 'No (3)': 3, 'No, 2': 2, 'No,4': 4, 'No( 2)': 2, 'No': 1, 'no (2)': 2, 'no respone': -1,
                        'no (3)': 3, 'no response': -1, 'no (1)': 1, 'no (4)': 4, 'no (2 missed)': 2, 'no (1 missed)': 1,
                        'no (4 missed)': 4, 'No (4 missed)': 4, 'no (missed one)': 1, 'no (missed 4)': 4, 'No (missed one)': 1,
                        'No (Missed 2)': 2, 'No (Missed 1)': 1, 'No (Missed 3)': 3, 'No (Missed 4)': 4, 'No; missed #1, #2,and #4': 3,
                        'No, missed #1': 1, 'No, missed #1 & #4': 2, 'No, missed #1 & #2': 2, 'No, missed #1, #3, and #4': 3,
                        'No; missed #1, #2, #3, and #4': 4, 'No, missed #2': 1, 'No, missed #1 and #2': 2, 'No, missed #3 & #4': 2,
                        'No, missed #2 & #3': 2, 'No, missed #2, #3, and #4': 3, 'No, 2/4': 2, 'No, 3/4': 1, 'No, 0/4': 4, 'No, 1/4': 3,
                        'No (2/4 incorect)': 2, 'No (4/4 incorrect)': 4, 'No (1/4 incorrect)': 1, 'No (3/4 incorrect)': 3,
                        'No (2/4 incorrect)': 2, 'No,1 missed': 1, 'No, 1 missed': 1, 'yes': 0, 'No, 2 missed': 2, 'No, 4 missed': 4,
                        'No, 1 Missed': 1, 'No,4 missed': 4, 'No. 2 wrong': 2, 'No, missed 1': 1, 'No. 1 missed': 1, 'No missed 4': 4,
                        'No, 3 missed': 3, 'No(2)': 2, 'No, 3 Wrong': 3, 'No, 1 wrong': 1, 'No, 4 wrong': 4, 'No, 2 Wrong': 2,
                        'No, 2 wrong': 2, '': -1, 'No, 3 wrong': 3, 'No, 4 Wrong': 4, 'No, 1 Wrong': 1, 'no, all wrong': 4, 'No, 1': 1,
                        '2 wrong': 2, 'no, 2': 2, 'all wrong': 4, 'no, 1': 1, 'all but 2 wrong': 2, 'no, 4': 4, 'no, two wrong': 2}

        self.group = 2
        return

    def numFore(self, iData):
        return self.numIMap[iData]

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(4 - oData)

#134 @all
class dataNotes(dataNaturalLanguage):
    def __init__(self):
        super(dataNotes, self).__init__()
        self.group = 11
        return

#135 StartDate.x
#136 EndDate
#137 NumberofDays
#138-169 Pool

#170 @test6
class dataClipBoardMaterial(dataChoice):
    def __init__(self):
        super(dataClipBoardMaterial, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'Plastic': 2, 'Metal': 1, 'NA': 0}
        self.numOMap = {0: 'NA', 1: 'Plastic', 2: 'Metal'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 3
        self.group = 6
        return

#171 @test4
class dataPersistence(dataPosInt):
    def __init__(self):
        super(dataPersistence, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData))

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData)

#172-218 order
#219 session_date
#220 DateComputer
#221 TimeComputer

#222 @test9
class dataMonthComputer(dataPosInt):
    def __init__(self):
        super(dataMonthComputer, self).__init__()
        self.group = 11
        return

#223 @test9
class dataDayComputer(dataPosInt):
    def __init__(self):
        super(dataDayComputer, self).__init__()
        self.group = 11
        return

#224 @test9
class dataYearComputer(dataPosInt):
    def __init__(self):
        super(dataYearComputer, self).__init__()
        self.group = 11
        return

#225 DaysSinceMonthComputer
#226 DaysSinceAugComputer
#227 Date.y
#228-232 date Lab
#233-238 date start
#239 DaysInComp
#240 DaysInLab
#241 AttentionCheck #...it is basically #9 #10

#242 @bigfive
class dataOpenness(dataPosInt):
    def __init__(self):
        super(dataOpenness, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return float(iData) * 2

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#243 @bigfive
class dataConscientiousness(dataPosInt):
    def __init__(self):
        super(dataConscientiousness, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return float(iData) * 2

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#244 @bigfive
class dataExtraversion(dataPosInt):
    def __init__(self):
        super(dataExtraversion, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return float(iData) * 2

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#245 @bigfive
class dataAgreeableness(dataPosInt):
    def __init__(self):
        super(dataAgreeableness, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return float(iData) * 2

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#246 @bigfive
class dataNeuroticism(dataPosInt):
    def __init__(self):
        super(dataNeuroticism, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 2)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#247 @Intrinsic
class dataIntrinsic(dataPosInt):
    def __init__(self):
        super(dataIntrinsic, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 15)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 15)

#248 @mood
class dataMood(dataPosInt):
    def __init__(self):
        super(dataMood, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 2)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 2)

#249 @NFC
class dataNFC(dataPosInt):
    def __init__(self):
        super(dataNFC, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 6)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 6)

#250 @all
class dataReportedAttention(dataPosInt):
    def __init__(self):
        super(dataReportedAttention, self).__init__()
        self.group = 0
        return

#251 @all
class dataReportedEffort(dataPosInt):
    def __init__(self):
        super(dataReportedEffort, self).__init__()
        self.group = 0
        return

#252 @test9
class dataSelfEsteem(dataPosInt):
    def __init__(self):
        super(dataSelfEsteem, self).__init__()
        self.group = 0
        return

#253 @all
class dataStress(dataPosInt):
    def __init__(self):
        super(dataStress, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 4)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 4)

#254 PowerCond

#255 @test10
class dataMostEndorse(dataPosInt):
    def __init__(self):
        super(dataMostEndorse, self).__init__()
        self.group = 10
        return

#256 @test10
class dataSomeEndorse(dataPosInt):
    def __init__(self):
        super(dataSomeEndorse, self).__init__()
        self.group = 10
        return

#257 @test10
class dataCredCond(dataChoice):
    def __init__(self):
        super(dataCredCond, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, 'NoCredentials': 0, 'Credentials': 1}
        self.numOMap = {-1: 'NA', 0: 'NoCredentials', 1: 'Credentials'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 10
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#258 @all
class dataGenderfactor(dataChoice):
    def __init__(self):
        super(dataGenderfactor, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, 'Female': 0, 'Male': 1}
        self.numOMap = {-1: 'NA', 0: 'Female', 1: 'Male'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#259 SubDistCond
#260-264 1st
#265-266 Avail
#267 TempCond4

#268 @all
class dataTempCond(dataChoice):
    def __init__(self):
        super(dataTempCond, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, 'Communal': 0, 'Agentic': 1}
        self.numOMap = {-1: 'NA', 0: 'Communal', 1: 'Agentic'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1
#269 @all
class dataTargetGender(dataChoice):
    def __init__(self):
        super(dataTargetGender, self).__init__()
        self.type = 'str / int / bool'
        self.numIMap = {'NA': -1, 'FemaleTarget': 0, 'MaleTarget': 1}
        self.numOMap = {-1: 'NA', 0: 'FemaleTarget', 1: 'MaleTarget'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.group = 0
        return

    def codeFore(self, iData):
        if iData == -1:
            return (self.real, False, False)
        else:
            return (self.real, True, bool(iData))

    def codeBack(self, oData):
        flag, data = oData
        if flag:
            return round(data)
        else:
            return -1

#270 @all
class dataArgumentQuality(dataPosInt):
    def __init__(self):
        super(dataArgumentQuality, self).__init__()
        self.group = 0
        return

    def numFore(self, iData):
        if iData == 'NA':
            return -1
        else:
            return round(float(iData) * 5)

    def numBack(self, oData):
        if oData == -1:
            return 'NA'
        else:
            return str(oData / 5)

#271 NFCcenter
#272 ELMCond
#273 CBReject

if __name__ == '__main__':
    a = datamcmost1()
    print(a.formatFore('1'))