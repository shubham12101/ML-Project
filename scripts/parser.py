import xml.etree.ElementTree as ET
from pprint import pprint
from lxml import etree
import codecs
from os import listdir
from os.path import isfile, join

# ==========CONSTANTS============

def appendRootNode(filename):
	f = codecs.open(filename,'r+', encoding='utf-8', errors='ignore')
	content = f.read()
	f.seek(0,0)
	f.write("<allreviews>".rstrip('\r\n') + '\n' + content)
	f.seek(-1,2)
	f.write("\n</allreviews>")
	f.close()

def combineFiles(outputFilepath, listOfFilepaths):
	flag = True
	for filename in listOfFilepaths:
		f = codecs.open(filename,'r', encoding='utf-8', errors='ignore')
		if flag == True:
			content = f.read()
			flag = False
		else:
			content = content + f.read()
		f.close()
	f1 = codecs.open(outputFilepath, 'w', encoding='utf-8', errors='ignore')
	f1.write(content)
	f1.close()


def extractData(filepath):
	fileName = filepath
	reviewTitleFilepath = filepath + '_title'
	reviewTextFilepath = filepath  +'_text'
	reviewRatingFilepath = filepath +'_rating'
	
	reviewTextList = []
	reviewRatingList = []
	reviewTitleList = []
	
	parser = etree.XMLParser(recover=True)
	tree = etree.parse(fileName, parser=parser)
	root = tree.getroot()

	# tree = ET.parse(filename)
	# root = tree.getroot()

	for review in root.findall('review'):
		reviewRating = review.find('rating')
		reviewRatingList.append(reviewRating.text.replace('\n',''))
		reviewTitle = review.find('title')
		reviewTitleList.append(reviewTitle.text.replace('\n',''))
		reviewText = review.find('review_text')
		reviewTextList.append(reviewText.text.replace('\n',''))

	print len(reviewTextList)
	
	f2 = codecs.open(reviewTitleFilepath,"w","utf-8")
	for title in reviewTitleList:
		f2.write(unicode(title)+'\n')
	f2.close()
	
	with codecs.open(reviewTextFilepath,"w","utf-8") as f1:
		for text in reviewTextList:
			f1.write(unicode(text)+'\n')

	with codecs.open(reviewRatingFilepath,"w","utf-8") as f3:
		for rating in reviewRatingList:
			f3.write(unicode(rating)+'\n')

if __name__ == '__main__':
	cls = 'negative'
	# cls = 'positive'	
	typ = 'type2'
	# # appendRootNode("../raw_data/categorical_data/positive_sports.review")
	# # strings = ["sports","electronics","music","software"]
	# # listOfFiles = ["../types/categorical_data/type1/camera_&_photo/"+typ+"_camera_&_photo.review","../raw_data/categorical_data/type1/cell_phones_&_service/negative_cell_phones_&_service.review","../raw_data/categorical_data/type1/computer_&_video_games/negative_computer_&_video_games.review","../raw_data/categorical_data/type1/dvd/negative_dvd.review","../raw_data/categorical_data/type1/electronics/negative_electronics.review"]
	listOfFiles = []
	filepath = "../types/"+typ+"/data/"
	for folder in listdir(filepath):		
		if isfile(folder):
			continue
		folderpath = filepath + folder
		print folderpath
		for f in listdir(folderpath):
			if cls in str(f):
				listOfFiles.append(join(folderpath, f))

	# print listOfFiles
	for name in listOfFiles:
		appendRootNode(name)
	completeName = join("../types/"+typ+"/raw_data/", typ+"_"+cls+".review") 
	print completeName
	combineFiles(completeName , listOfFiles)
	# appendRootNode("../raw_data/categorical_data/negative_sports.review")
	extractData(completeName)
