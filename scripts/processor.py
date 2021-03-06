import nltk
import spellchecker
import re
import math
import codecs
import csv
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
bigram_counter_class1 = Counter()
bigram_counter_class2 = Counter()
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
    # print text
    array = get_empty_array(len(bag_of_words))
    for i in range(0, len(bag_of_words), 1):
        # print bag_of_words[i]
        array[i] = text.count(bag_of_words[i])
    return array

def get_bigram_array(text, bag_of_bigram):
    array = get_empty_array(len(bag_of_bigram))
    for i in range(0, len(bag_of_bigram), 1):
        array[i] = text.count(bag_of_bigram[i])
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
            dictionary = {word: count}
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
        return ''

def getNGrams(text, n):
    blob = TextBlob(text)
    listofBlobs = blob.ngrams(n)
    listofBigrams = []
    for wordList in listofBlobs:
        flag = True
        for item in wordList:
            if flag:
                bigram = unicode(item)
                flag = False
            else:
                bigram = bigram + " "+ unicode(item)
        # print type(bigram)
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

def get_ngram_count(filename, ngram_counter, n):
    # f = codecs.open(filename, "r","utf-8")
    # array = f.readlines()
    # print type(array)
    array = getDataFromFile(filename)
    for text in array:
        text = re.sub(' +', " ", text)
    for text in array:
        list = getNGrams(text, n)
        for ngram in list:
            print ngram
            count = 0
            for line in array:                
                if ngram in line:
                    count = count + 1
            dictionary = {ngram: count}
            ngram_counter.update(dictionary)
    return ngram_counter

def getDataFromFile(filename):
    f = codecs.open(filename, 'r',encoding='utf-8', errors='ignore')
    dataList = []
    for line in f:
        dataList.append(line)
    f.close()
    return dataList

def writeDataToFile(filename, dataList):
    f = codecs.open(filename, 'wb', 'utf-8')
    for data in dataList:
        f.write(unicode(data+"\n"))
    f.close()
    return dataList

def processData(fileFrom, fileTo):
    print fileFrom
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
    pprint(listofText)
    writeDataToFile(filename=fileTo, dataList=listofText)

def generate_word_list(counter1 , counter2):
    list = []
    list_positive = counter1.most_common(100)
    list_negative = counter2.most_common(100)
    for t in list_positive:
        list.append(t[0])
    for t in list_negative:
        list.append(t[0])
    return list

def write_array_to_csv(output_file, arr):
    with open(output_file, "wb") as output:
        writer = csv.writer(output)
        writer.writerows(arr)

def create_test_label_file(input_file, output_file):
    input_data = getDataFromFile(input_file)
    output = []
    for input in input_data:
        input = float(input)
        if(input > 3):
            output.append('1')
        else:
            output.append('0')
    write_data_to_file(output_file, output)

def create_positive_test_label_file(input_file, output_file):
    input_data = getDataFromFile(input_file)
    output = []
    for input in input_data:
        input = float(input)
        if(input == 5):
            output.append('1')
        elif (input == 4):
            output.append('0')
    write_data_to_file(output_file, output)

def create_negative_test_label_file(input_file, output_file):
    input_data = getDataFromFile(input_file)
    output = []
    for input in input_data:
        input = float(input)
        if(input == 2):
            output.append('1')
        elif (input == 1):
            output.append('0')
    write_data_to_file(output_file, output)

def write_data_to_file(filename, dataList):
    f = codecs.open(filename, 'w', encoding='utf-8', errors='ignore')
    for data in dataList:
        # f.write(unicode((str(data.rstrip('\r\n'))+"\n")))
        f.write(data.rstrip('\r\n')+"\n")
    f.close()
    return dataList

def getPositiveStarredReviews(positiveReview, fiveStarredFile, fourStarredFile, labelFile, positiveStarredLabelFile):
    input_data = getDataFromFile(labelFile)
    review_data = getDataFromFile(positiveReview)

    fiveStarredList = []
    fourStarredList = []
    positiveStarredLabelList = []
    i = 0
    for item in input_data:
        item = float(item)
        if(item == 5):
            fiveStarredList.append(review_data[i])
            positiveStarredLabelList.append('1')
        else:
            fourStarredList.append(review_data[i])
            positiveStarredLabelList.append('0')
        i += 1
    write_data_to_file(fiveStarredFile, fiveStarredList)
    write_data_to_file(fourStarredFile, fourStarredList)
    write_data_to_file(positiveStarredLabelFile, positiveStarredLabelList)

def getNegativeStarredReviews(negativeReview, twoStarredFile, oneStarredFile, labelFile, negativeStarredLabelFile):
    input_data = getDataFromFile(labelFile)
    review_data = getDataFromFile(negativeReview)

    twoStarredList = []
    oneStarredList = []
    negativeStarredLabelList = []
    i = 0
    for item in input_data:
        item = float(item)
        if(item == 2):
            twoStarredList.append(review_data[i])
            negativeStarredLabelList.append('1')
        else:
            oneStarredList.append(review_data[i])
            negativeStarredLabelList.append('0')
        i += 1
    write_data_to_file(twoStarredFile, twoStarredList)
    write_data_to_file(oneStarredFile, oneStarredList)
    write_data_to_file(negativeStarredLabelFile, negativeStarredLabelList)


if __name__ == '__main__':
    typ = 'type5'
    folderpath = "../types/" + typ + "/"
    processData(folderpath + "raw_data/" + typ + "_unlabeled.review_text", folderpath + "processed_data/" + typ + "_unlabeled.review_text")
    getPositiveStarredReviews(folderpath + "raw_data/" + typ + "_positive.review_text",folderpath + "raw_data/" + typ + "_fivestarred.review_text",folderpath + "raw_data/" + typ + "_fourstarred.review_text", folderpath + "raw_data/" + typ + "_positive.review_rating",folderpath + "processed_data/" + typ + "_positive_starred.review_labels")
    getNegativeStarredReviews(folderpath + "raw_data/" + typ + "_negative.review_text",folderpath + "raw_data/" + typ + "_twostarred.review_text",folderpath + "raw_data/" + typ + "_onestarred.review_text", folderpath + "raw_data/" + typ + "_negative.review_rating",folderpath + "processed_data/" + typ + "_negative_starred.review_labels")

    processData(folderpath + "raw_data/" + typ + "_negative.review_text", folderpath + "processed_data/" + typ + "_negative.review_text")
    processData(folderpath + "raw_data/" + typ + "_positive.review_text",folderpath + "processed_data/" + typ + "_positive.review_text")
    get_ngram_count(folderpath + "processed_data/" + typ + "_positive.review_text", bigram_counter_class1, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_negative.review_text", bigram_counter_class2, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_positive.review_text", word_counter_class1, 1)
    get_ngram_count(folderpath + "processed_data/" + typ + "_negative.review_text", word_counter_class2, 1)   
    bag_of_words = generate_word_list(word_counter_class1, word_counter_class2)
    bag_of_bigrams = generate_word_list(bigram_counter_class1, bigram_counter_class2)    
    writeDataToFile(folderpath + "processed_data/" + typ +"_bag_of_words.list",bag_of_words)
    writeDataToFile(folderpath + "processed_data/" + typ +"_bag_of_bigrams.list",bag_of_bigrams)

    processData(folderpath + "raw_data/" + typ + "_fourstarred.review_text", folderpath + "processed_data/" + typ + "_fourstarred.review_text")
    processData(folderpath + "raw_data/" + typ + "_fivestarred.review_text",folderpath + "processed_data/" + typ + "_fivestarred.review_text")
    get_ngram_count(folderpath + "processed_data/" + typ + "_fourstarred.review_text", bigram_counter_class1, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_fivestarred.review_text", bigram_counter_class2, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_fourstarred.review_text", word_counter_class1, 1)
    get_ngram_count(folderpath + "processed_data/" + typ + "_fivestarred.review_text", word_counter_class2, 1)
    bag_of_words = generate_word_list(word_counter_class1, word_counter_class2)
    bag_of_bigrams = generate_word_list(bigram_counter_class1, bigram_counter_class2)    
    writeDataToFile(folderpath + "processed_data/" + typ +"_positive_starred_bag_of_words.list",bag_of_words)
    writeDataToFile(folderpath + "processed_data/" + typ +"_positive_starred_bag_of_bigrams.list",bag_of_bigrams)

    processData(folderpath + "raw_data/" + typ + "_onestarred.review_text", folderpath + "processed_data/" + typ + "_onestarred.review_text")
    processData(folderpath + "raw_data/" + typ + "_twostarred.review_text",folderpath + "processed_data/" + typ + "_twostarred.review_text")
    get_ngram_count(folderpath + "processed_data/" + typ + "_onestarred.review_text", bigram_counter_class1, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_twostarred.review_text", bigram_counter_class2, 2)
    get_ngram_count(folderpath + "processed_data/" + typ + "_onestarred.review_text", word_counter_class1, 1)
    get_ngram_count(folderpath + "processed_data/" + typ + "_twostarred.review_text", word_counter_class2, 1)
    bag_of_words = generate_word_list(word_counter_class1, word_counter_class2)
    bag_of_bigrams = generate_word_list(bigram_counter_class1, bigram_counter_class2)    
    writeDataToFile(folderpath + "processed_data/" + typ +"_negative_starred_bag_of_words.list",bag_of_words)
    writeDataToFile(folderpath + "processed_data/" + typ +"_negative_starred_bag_of_bigrams.list",bag_of_bigrams)
