import nltk
import spellchecker
import re
import math
import codecs
from collections import Counter
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
from pprint import pprint

word_counter_class1 = Counter()
word_counter_class2 = Counter()
ngram_counter_class1 = Counter()
ngram_counter_class2 = Counter()
count_class1 = 0
count_class2 = 0

def create_term_frequency(file1, file2):
    get_document_term_frequency(file1, word_counter_class1)
    get_document_term_frequency(file2, word_counter_class2)
    count_class1 = get_number_of_lines_in_file(file1)
    count_class2 = get_number_of_lines_in_file(file2)

def get_number_of_lines_in_file(file):
    f = open(file)
    return len(f.readlines())

def lemmatizer(word):
    """

    :param word:
    :return:
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    return wordnet_lemmatizer.lemmatize(word)

def stemmer(text):
    pStemmer = PorterStemmer()
    return pStemmer.stem(text)

def tagger(text):
    """

    :param text:
    :return:
    """
    token_text = nltk.word_tokenize(text)
    tagged_list = nltk.pos_tag(token_text)
    return tagged_list

def spell_check(text):
    """

    :param text:
    :return:
    """
    token_text = tokenise(text)
    # print token_text
    for word in token_text:
        # print word
        correct_word = spellchecker.correct(word)
        # print correct_word
        text = text.replace(word, correct_word)
    # print text
    return text

def tokenise(text):
    token_text = text.split(' ')
    return token_text

def get_array_string(list):
    string = str(list)
    string = remove_brackets_from_string(string)
    return string

def remove_brackets_from_string(string):
    result = string.replace("[", "")
    result = result.replace("]", "")
    return result

def get_empty_array(size):
    list = []
    for i in range(0,size,1):
        list.append(0)
    return list

def get_tf_if_array(text, frequent_word_list):
    array = get_empty_array(len(frequent_word_list))
    for i in range(0, len(frequent_word_list), 1):
        array[i] = get_tf_if(frequent_word_list[i], text)
    return array

def get_bag_of_words_array(text, bag_of_words):
    array = get_empty_array(len(bag_of_words))
    for i in range(0, len(bag_of_words), 1):
        array[i] = text.count((bag_of_words[i], text))
    return array

def get_bigram_array(text, bag_of_bigram):
    array = get_empty_array(len(bag_of_bigram))
    for i in range(0, len(bag_of_bigram), 1):
        array[i] = get_tf_if(bag_of_bigram[i], text)
    return array

def get_term_frequency(word, document):
    if word in document:
        return document.count(word)
    else:
        return 0

def get_tf_if(word, document):
    tf = get_term_frequency(word, document)
    inverse_frequency = get_inverse_document_term_frequency(word)
    return tf * inverse_frequency

def get_document_term_frequency(filename, word_counter):
    f = open(filename, 'r')
    array = f.readlines()
    for line in array:
        word_list = re.sub("[^\w]", " ",  line).split()
        for word in word_list:
            count = 0
            for item in array:
                if word in item:
                    count = count + 1
            dictionary = {word, count}
            word_counter.update(dictionary)
    # print word_counter
    f.close()
    return word_counter

def get_inverse_document_term_frequency(word):
    word_counter_dictionary = dict(word_counter_class1)
    word_count = word_counter_dictionary.get(word, default=0)
    frequency = float(word_count/count_class1)
    frequency = 1/frequency
    log = math.log(frequency, math.e)
    # print log
    return log

def remove_stop_words_from_string(string):
    # Remove stop words
    cachedStopWords = stopwords.words("english")
    desiredWords = ['not','nor','no','than','very']
    for word in desiredWords:
        cachedStopWords.remove(word)
    clean_string = ' '.join([word for word in string.split() if word not in cachedStopWords])
    return clean_string

def removePunc(text):
    emoticonList = [":)", ":-)", ":(", ":-(", ":')", ":'(", ":D", ":-D", ":P", ":p", ":-p", ":P", ":*", ";)", ";-)", ";(", ";-(", "B)", "B-)"]
    tknzr = TweetTokenizer()
    listOfTokens = tknzr.tokenize(text)
    flag = True
    for item in listOfTokens:
        if (item.isalpha() or (item in emoticonList)):
            if flag:
                newText = item.lower()
                flag = False
            else:
                newText = newText + " " + unicode(item).lower()
    if not flag:
        return newText
    else:
        return None

def getNGrams(text, n):
    blob = TextBlob(text)
    listofBlobs = blob.ngrams(n)
    listofBigrams = []
    for wordList in listofBlobs:
        flag = True
        for item in wordList:
            if flag:
                bigram = item
                flag = False
            else:
                bigram = bigram + " "+ unicode(item)
        listofBigrams.append(bigram)
    return listofBigrams

def getWordCount(filename):
    f = open(filename, 'r')
    wordcount = Counter(f.read().split())
    return wordcount

def getMostFreqWordsList(filename, ctr):
    wordCounter = getWordCount(filename)
    mostCommonWordList = wordCounter.most_common(ctr)
    mostFreqWordsList = []
    for word in mostCommonWordList:
        mostFreqWordsList.append(word[0])
    return mostFreqWordsList

def get_ngram_count(filename, ngram_counter):
    # f = codecs.open(filename, "r","utf-8")
    # array = f.readlines()
    # print type(array)
    array = getDataFromFile(filename)
    for text in array:
        text = re.sub(' +', " ", text)
        # print text
    for text in array:
        print text
        list = getNGrams(text, 2)
        # print list
        for ngram in list:
            count = 0
            print ngram
            for line in array:
                if ngram in line:
                    count = count + 1
            dictionary = {ngram, count}
            ngram_counter.update(dictionary)
    print ngram_counter
    return ngram_counter

def getDataFromFile(filename):
    f = codecs.open(filename, 'r','utf-8')
    dataList = []
    for line in f:
        dataList.append(line)
    f.close()
    return dataList

def writeDataToFile(filename, dataList):
    f = codecs.open(filename, 'w', 'utf-8')
    for data in dataList:
        f.write(unicode(data+"\n"))
    f.close()
    return dataList

def processData(fileFrom, fileTo):
    textList = getDataFromFile(fileFrom)
    listofText = []
    for text in textList:
        if text != "\n":
            text1 = removePunc(text)
            text1 = remove_stop_words_from_string(text1)
            # text1 = spell_check(text1)
            text1 = lemmatizer(text1)
            # text1 = stemmer(text1)
            listofText.append(text1)
    # pprint(listofText)
    writeDataToFile(filename=fileTo, dataList=listofText)

if __name__ == '__main__':

    get_ngram_count("/home/shiv/ML/ML-Project/processed_data/positive.review_text", ngram_counter_class1)
    # processData("../raw_data/positive.review_text","../processed_data/positive.review_text")
    # print spell_check("The big fst boy")
    # get_term_frequency("/home/shiv/ML/ML-Project/raw_data/negative.review_text")
    # get_inverse_document_term_frequency("/home/shiv/ML/ML-Project/raw_data/positive.review_text")

