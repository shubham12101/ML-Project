import nltk
import spellchecker
from autocorrect import spell
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

def lemmatizer(word):
    """

    :param word:
    :return:
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    return wordnet_lemmatizer.lemmatize(word)

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
    token_text = tokenize(text)
    # print token_text
    for word in token_text:
        # print word
        correct_word = spellchecker.correct(word)
        # print correct_word
        text = text.replace(word, correct_word)
    # print text
    return text

def tokenize(text):
    token_text = text.split(' ')
    return token_text

def removePunc(text):
    emoticonList = [":)", ":-)", ":(", ":-(", ":')", ":'(", ":D", ":-D", ":P", ":p", ":-p", ":P", ":*", ";)", ";-)", ";(", ";-(", "B)", "B-)"]
    tknzr = TweetTokenizer()
    listOfTokens = tknzr.tokenize(text)
    flag = True
    for item in listOfTokens:
        if (item.isalnum() or (item in emoticonList)):
            if flag:
                newText = item.lower()
                flag = False
            else:
                newText = newText + " " + unicode(item).lower()
    return newText

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


if __name__ == '__main__':
    kandi = removePunc("I am Kandi!!!! And I know it, do you? ;)")
    print getNGrams(text=kandi, n=2)
