class dataCol(object):
    def __init__(self):
        # self.numIMap = dict()
        # self.numOMap = dict()
        # self.codeIMap = dict()
        # self.codeOMap = dict()
        self.type = 'unknown'
        return

    def numFore(self, iData):
        return iData

    def numBack(self, oData):
        return oData

    def codeFore(self, iData):
        return iData

    def codeBack(self, oData):
        return oData

    def formatFore(self, iData):
        return self.codeFore(self.numFore(iData))

    def formatBack(self, oData):
        return self.numBack(self.codeBack(oData))

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__ + ': ' + self.type

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
        oData = [False for i in range(self.iMapSize)]
        oData[iData] = True
        return oData

    def codeBack(self, oData):
        for i in range(self.oMapSize):
            if oData[i]:
                return i
        else:
            print('E: ' + repr(self) + ', codeBack: invalid oData.')
            return None

#positive int for ID
class dataPosInt(dataCol):
    def __init__(self):
        super(dataPosInt, self).__init__()
        self.type = 'str / int / [bool, int]'
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
            return [False, 0]
        else:
            return [True, iData]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return iData
        else:
            return -1

#true answer
class dataTrueAnswer(dataCol):
    def __init__(self):
        super(dataTrueAnswer, self).__init__()
        self.type = 'str / int / [bool, bool]'
        self.iAns = ''
        self.oAns = ''

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
            return [False, False]
        else:
            return [True, bool(iData)]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return int(iData)
        else:
            return -1

class dataNaturalLanguage(dataCol):
    def __init__(self):
        super(dataCol, self).__init__()
        self.type = 'str / int / bool'
        return

    def numFore(self, iData):
        return int(iData != 'NA') 

    def numBack(self, oData):
        if oData == 0:
            return 'NA'
        else:
            return 'someString'

    def codeFore(self, iData):
        return bool(iData)

    def codeBack(self, oData):
        return int(oData)


class dataBool(dataCol):
    def __init__(self):
        super(dataBool, self).__init__()
        self.type = 'str / int / bool'
        self.validStr = ''
        return

    def numFore(self, iData):
        return int(iData != 'NA') 

    def numBack(self, oData):
        if oData == 0:
            return 'NA'
        else:
            return self.validStr

    def codeFore(self, iData):
        return bool(iData)

    def codeBack(self, oData):
        return int(oData)



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
        return

#1
class dataParticipant_ID(dataPosInt):
    def __init__(self):
        super(dataParticipant_ID, self).__init__()
        return

#2
class dataRowNumber(dataPosInt):
    def __init__(self):
        super(dataRowNumber, self).__init__()
        return

#3
class datasession_id(dataPosInt):
    def __init__(self):
        super(datasession_id, self).__init__()
        return

#4
class dataage(dataCol):
    def __init__(self):
        super(dataage, self).__init__()
        self.type = 'str / int / [bool, int]'

        self.numIMap = {'NA': -1, '18 almost 19': 19, '22 years': 22, 'almost 19': 19, 'Too Old (18)': 18, '18 years': 18,
                        '19.5': 19, '20`': 20, 'we': -1, '-2': -1, 'almost 18': 18, '17 (18 in one month)': 18}
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
            return [False, 0]
        else:
            return [True, iData]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return iData
        else:
            return -1

#5 @persistance @test4
class dataanagrams1(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams1, self).__init__()
        self.iAns = 'party'
        self.oAns = 'party'
        return

#6 @persistance @test4
class dataanagrams2(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams2, self).__init__()
        self.iAns = 'fatal'
        self.oAns = 'fatal'
        return

#7 @persistance @test4
class dataanagrams3(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams3, self).__init__()
        self.iAns = None
        self.oAns = 'notAWord'
        return

#8 @persistance @test4
class dataanagrams4(dataTrueAnswer):
    def __init__(self):
        super(dataanagrams4, self).__init__()
        self.iAns = None
        self.oAns = 'notAWord'
        return

#9 ~@test3
#anyway, maybe it reflects some traits about this person
class dataattention(dataChoice):
    def __init__(self):
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}

        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
        return

#10 ~@test3
class dataattentioncorrect(dataChoice):
    def __init__(self):
        super(dataattentioncorrect, self).__init__()
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
        return

    def codeFore(self, iData):
        if iData == -1:
            return [False, False]
        else:
            return [True, bool(iData)]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return int(iData)
        else:
            return -1

#11 @test5
class databackcount1(dataTrueAnswer):
    def __init__(self):
        super(databackcount1, self).__init__()
        self.iAns = '357'
        self.oAns = '357'
        return

#12 @test5
class databackcount10(dataTrueAnswer):
    def __init__(self):
        super(databackcount10, self).__init__()
        self.iAns = '330'
        self.oAns = '330'
        return

#13 @test5
class databackcount2(dataTrueAnswer):
    def __init__(self):
        super(databackcount2, self).__init__()
        self.iAns = '354'
        self.oAns = '354'
        return

#14 @test5
class databackcount3(dataTrueAnswer):
    def __init__(self):
        super(databackcount3, self).__init__()
        self.iAns = '351'
        self.oAns = '351'
        return

#15 @test5
class databackcount4(dataTrueAnswer):
    def __init__(self):
        super(databackcount4, self).__init__()
        self.iAns = '348'
        self.oAns = '348'
        return

#16 @test5
class databackcount5(dataTrueAnswer):
    def __init__(self):
        super(databackcount5, self).__init__()
        self.iAns = '345'
        self.oAns = '345'
        return

#17 @test5
class databackcount6(dataTrueAnswer):
    def __init__(self):
        super(databackcount6, self).__init__()
        self.iAns = '342'
        self.oAns = '342'
        return

#18 @test5
class databackcount7(dataTrueAnswer):
    def __init__(self):
        super(databackcount7, self).__init__()
        self.iAns = '339'
        self.oAns = '339'
        return

#19 @test5
class databackcount8(dataTrueAnswer):
    def __init__(self):
        super(databackcount8, self).__init__()
        self.iAns = '336'
        self.oAns = '336'
        return

#20 @test5
class databackcount9(dataTrueAnswer):
    def __init__(self):
        super(databackcount9, self).__init__()
        self.iAns = '333'
        self.oAns = '333'
        return

#21 @test9
class databestgrade1(dataCol):
    def __init__(self):
        super(databestgrade1, self).__init__()
        self.type = 'str / (int, int) / [bool, (int, int)]'
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
            return [False, (0, 0)]
        else:
            return [True, iData]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return iData
        else:
            return (-1, -1)

#22 ~@test9
class databestgrade2(dataCol):
    def __init__(self):
        super(databestgrade2, self).__init__()
        self.type = 'str / int / [bool, int]'
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
            return [False, 0]
        else:
            return [True, iData]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return iData
        else:
            return -1

#23 @test9
class databestgrade3(dataPosInt):
    def __init__(self):
        super(databestgrade3, self).__init__()
        return

#24 @test9
class databestgrade4(dataPosInt):
    def __init__(self):
        super(databestgrade4, self).__init__()
        return

#25 @test9
class databestgrade5(dataPosInt):
    def __init__(self):
        super(databestgrade5, self).__init__()
        return

#26 @test4
class databig5_01(dataPosInt):
    def __init__(self):
        super(databig5_01, self).__init__()
        return

#27 @test4
class databig5_02(dataPosInt):
    def __init__(self):
        super(databig5_02, self).__init__()
        return

#28 @test4
class databig5_03(dataPosInt):
    def __init__(self):
        super(databig5_03, self).__init__()
        return

#29 @test4
class databig5_04(dataPosInt):
    def __init__(self):
        super(databig5_04, self).__init__()
        return

#30 @test4
class databig5_05(dataPosInt):
    def __init__(self):
        super(databig5_05, self).__init__()
        return

#31 @test4
class databig5_06(dataPosInt):
    def __init__(self):
        super(databig5_06, self).__init__()
        return

#32 @test4
class databig5_07(dataPosInt):
    def __init__(self):
        super(databig5_07, self).__init__()
        return

#33 @test4
class databig5_08(dataPosInt):
    def __init__(self):
        super(databig5_08, self).__init__()
        return

#34 @test4
class databig5_09(dataPosInt):
    def __init__(self):
        super(databig5_09, self).__init__()
        return

#35 @test4
class databig5_10(dataPosInt):
    def __init__(self):
        super(databig5_10, self).__init__()
        return

#36 ~@test5
class datadiv3filler(dataCol):
    def __init__(self):
        super(datadiv3filler, self).__init__()
        self.type = 'str / int / [bool, bool]'
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
            return [False, False]
        else:
            return [True, bool(iData)]

    def codeBack(self, oData):
        flag, iData = oData
        if flag is True:
            return int(iData)
        else:
            return -1

#37 @test8
class dataelm_01(dataPosInt):
    def __init__(self):
        super(dataelm_01, self).__init__()
        return

#38 @test8
class dataelm_02(dataPosInt):
    def __init__(self):
        super(dataelm_02, self).__init__()
        return

#39 @test8
class dataelm_03(dataPosInt):
    def __init__(self):
        super(dataelm_03, self).__init__()
        return

#40 @test8
class dataelm_04(dataPosInt):
    def __init__(self):
        super(dataelm_04, self).__init__()
        return

#41 @test8
class dataelm_05(dataPosInt):
    def __init__(self):
        super(dataelm_05, self).__init__()
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
        return

    def numBack(self, oData):
        return self.numOMap[oData]

#43 @test1
class datafeedback(dataBool):
    def __init__(self):
        super(datafeedback, self).__init__()
        self.validStr = 'This Stroop task has no feedback'

#44 @demographics
class datagender(dataChoice):
    def __init__(self):
        super(datagender, self).__init__()
        self.numIMap = {'NA': 0, '1': 1, '2': 2, '19': 3, 'Agender': 4, '3': 3, 'Gender Fluid': 4, 'gender neutral': 4, 'Alien': 4}
        self.numOMap = {0: 'NA', 1: '1', 2: '2', 3: '3', 4: 'others'}

        self.iMapSize, self.oMapSize = self._getMapSize()
        self.iMapSize = 5
        self.defaultNum = 4
        return

#45 @test5
class datahighpower(dataNaturalLanguage):
    def __init__(self):
        super(datahighpower, self).__init__()
        return

#46 @test4
class datainstructbig5(dataBool):
    def __init__(self):
        super(datainstructbig5, self).__init__()
        self.validStr = '1'

if __name__ == '__main__':
    a = datainstructbig5()
    print(a.formatFore('NA'))