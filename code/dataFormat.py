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
		return

	def _getMapSize(self):
		return (len(self.numIMap), len(self.numOMap))

	def numFore(self, iData):
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
		super(databackcount1, self).__init__()
		self.iAns = '330'
		self.oAns = '330'
		return

#13 @test5
class databackcount2(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '354'
		self.oAns = '354'
		return

#14 @test5
class databackcount3(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '351'
		self.oAns = '351'
		return

#15 @test5
class databackcount4(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '348'
		self.oAns = '348'
		return

#16 @test5
class databackcount5(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '345'
		self.oAns = '345'
		return

#17 @test5
class databackcount6(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '342'
		self.oAns = '342'
		return

#18 @test5
class databackcount7(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '339'
		self.oAns = '339'
		return

#19 @test5
class databackcount8(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '336'
		self.oAns = '336'
		return

#20 @test5
class databackcount9(dataTrueAnswer):
	def __init__(self):
		super(databackcount1, self).__init__()
		self.iAns = '333'
		self.oAns = '333'
		return


if __name__ == '__main__':
	a = databackcount1()
	print(a.formatFore('NA'))