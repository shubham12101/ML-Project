import csv
import processor as Processor

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

if __name__ == '__main__':
    # Processor.processData("../raw_data/unlabeled.review_text", "../processed_data/unlabeled.review_text")
    extract_features_from_file("../processed_data/unlabeled.review_text", "../processed_data/test_features.csv")
    # bag_of_words =  file_to_array("../processed_data/bag_of_bigrams.list")
    # bag_of_bigrams =  file_to_array("../processed_data/bag_of_bigrams.list")

    # array1 = Processor.getDataFromFile("../processed_data/positive.review_text")
    # array2 = Processor.getDataFromFile("../processed_data/negative.review_text")
    
    # array = []
    # for line in array1:
    #     bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
    #     bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
    #     array.append(bag_of_words_array + bag_of_bigrams_array)
    
    # for line in array2:
    #     bag_of_words_array = Processor.get_bag_of_words_array(line, bag_of_words)
    #     bag_of_bigrams_array = Processor.get_bigram_array(line, bag_of_bigrams)
    #     array.append(bag_of_words_array + bag_of_bigrams_array)
    
    # with open("../processed_data/features.csv", "wb") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(array)