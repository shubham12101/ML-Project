import xml.etree.ElementTree as ET
from pprint import pprint
from lxml import etree
import codecs

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


def extractData(reviewType):
	fileName = '../raw_data/'+reviewType+'.review'
	reviewTitleFilepath = '../raw_data/'+reviewType+'.review_title'
	reviewTextFilepath = '../raw_data/'+reviewType+'.review_text'
	reviewRatingFilepath = '../raw_data/'+reviewType+'.review_rating'
	
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
	# appendRootNode("../raw_data/categorical_data/positive_sports.review")
	# strings = ["sports","electronics","music","software"]
	# listOfFiles = ["../raw_data/categorical_data/positive_sports.review","../raw_data/categorical_data/positive_electronics.review","../raw_data/categorical_data/positive_music.review","../raw_data/categorical_data/positive_software.review"]
	# for name in listOfFiles:
		# appendRootNode(name)
	# combineFiles("../raw_data/positive.review",listOfFiles)
	appendRootNode("../raw_data/categorical_data/negative_sports.review")
	extractData(reviewType = "/categorical_data/negative_sports")
