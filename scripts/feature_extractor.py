import csv
import processor as Processor
from pprint import pprint

__author__ = 'shiv'

def extract_features_from_file(input_file, output_file):
    bag_of_words =  file_to_array("../processed_data/bag_of_bigrams.list")
    bag_of_bigrams =  file_to_array("../processed_data/bag_of_bigrams.list")

    data = Processor.getDataFromFile(input_file)

    output = []
    for line in data:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        output.append(bag_of_words_array + bag_of_bigrams_array)

    Processor.write_array_to_csv(output_file, output)

def file_to_array(input_file):
    f = open(input_file, 'r')
    array = []
    for line in f.readlines():
        line = line.replace('\n', '')
        array.append(line)
    return array

def commonStopWordsList(array):
    temp = array[100:199]
    common = []
    for i in range(0,99):
        if array[i] in temp:
            common.append(array[i])
    return common   

if __name__ == '__main__':

    typ = 'type1'
    folderpath = "../types/" + typ + "/processed_data/"+typ+"_"

    cat = 'positive'
    bag_of_words =  file_to_array(folderpath + cat  + "_starred_bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + cat  + "_starred_bag_of_bigrams.list")
    array1 = Processor.getDataFromFile(folderpath + "fourstarred.review_text")
    array2 = Processor.getDataFromFile(folderpath + "fivestarred.review_text")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    for line in array2:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    with open(folderpath +  cat + "_starred_features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

    print("+ve")
    pprint(commonStopWordsList(bag_of_words))

    cat = 'negative'
    bag_of_words =  file_to_array(folderpath + cat  + "_starred_bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + cat  + "_starred_bag_of_bigrams.list")
    array1 = Processor.getDataFromFile(folderpath + "onestarred.review_text")
    array2 = Processor.getDataFromFile(folderpath + "twostarred.review_text")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    for line in array2:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    with open(folderpath +  cat + "_starred_features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

    print("-ve")
    pprint(commonStopWordsList(bag_of_words))

    array1 = Processor.getDataFromFile(folderpath + "positive.review_text")
    array2 = Processor.getDataFromFile(folderpath + "negative.review_text")
    bag_of_words =  file_to_array(folderpath + "bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + "bag_of_bigrams.list")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)    
    print len(array)
    for line in array2:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    print len(array)
    with open(folderpath + "features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

    print("All")
    pprint(commonStopWordsList(bag_of_words))

    cat = 'positive'
    bag_of_words =  file_to_array(folderpath + cat  + "_starred_bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + cat  + "_starred_bag_of_bigrams.list")
    array1 = Processor.getDataFromFile(folderpath + "unlabeled.review_text")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    with open(folderpath + "unlabelled_positive_starred_features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

    cat = 'negative'
    bag_of_words =  file_to_array(folderpath + cat  + "_starred_bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + cat  + "_starred_bag_of_bigrams.list")
    array1 = Processor.getDataFromFile(folderpath + "unlabeled.review_text")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    with open(folderpath + "unlabelled_negative_starred_features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

    bag_of_words =  file_to_array(folderpath + "bag_of_words.list")
    bag_of_bigrams =  file_to_array(folderpath  + "bag_of_bigrams.list")
    array1 = Processor.getDataFromFile(folderpath + "unlabeled.review_text")
    array = []
    for line in array1:
        bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
        bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
        array.append(bag_of_words_array + bag_of_bigrams_array)
    with open(folderpath + "unlabelled_features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(array)

