import re
import json
stop_word_file = "SmartStopList.txt"
import spacy

def getKeyWords(text):
    #breaks up text into phrases by puntuation
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)

    #makes a list of stop words from SmartStoplist.txt
    stop_words  = []
    for line in open(stop_word_file):
        stop_words.append(line[:-1])

    #makes the regex for the stop words
    stop_word_regex_list = []
    for word in stop_words:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
        stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)

    #seperates the sentences by stop words
    phrase_list = [] 
    for sentence in sentences:
        tmp = re.sub(stop_word_pattern, '|', sentence.strip())  
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)

    word_frequency = {}
    word_degree = {}
    for phrase in phrase_list:
        word_list_length = len(phrase.split(" "))
        word_list_degree = word_list_length - 1
        for word in phrase.split(" "):
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.

    #calculates word scores : word score = word frequency + word degree / (word frequency * 1.0)
    word_score = {}
    for word in word_frequency:
        word_score.setdefault(word, 0)
        word_score[word] =  (word_degree[word]+ word_frequency[word]) / (word_frequency[word] * 1.0)

    #sums word scores for each phrase
    phrase_score = {}
    for phrase in phrase_list:
        phrase_score.setdefault(phrase, 0)
        for word in phrase.split(" "):
            phrase_score[phrase] += word_score[word]

    #returns a list of phrases with scores
    return phrase_score


# data = ""

songs = {}

def query(query):
    for i in range(1950, 2015):
        with open('data/' + str(i) + '.json') as data_file:  
            data_set = json.load(data_file)
            for i in range(0, len(data_set)):
                data = [data_set[i]]
                if( query == data[0]['title']  ):
                    songs[data[0]['title'] ] = getKeyWords(data[0]['lyrics'])
                    return

    print("Song not found")


import sys

query(sys.argv[1])
print(sys.argv[1])

song_list = (songs.keys())

nlp = spacy.load('en')


palette = {}

for song in song_list:
    word_count = 0
    colors = {}
    colors['red'] = 0
    colors['green'] = 0
    colors['blue'] = 0
    
    for word in songs[song]:
        word_count += 1
        w2 = nlp(word)

        w1 = nlp(unicode("red"))
        similarity_rating = w1.similarity(w2)
        colors["red"] = similarity_rating / songs[song][word]

        w1 = nlp(unicode("orange"))
        similarity_rating = w1.similarity(w2)
        colors["orange"] = similarity_rating / songs[song][word]

        w1 = nlp(unicode("yellow"))
        similarity_rating = w1.similarity(w2)
        colors["yellow"] = similarity_rating / songs[song][word]

        w1 = nlp(unicode("green"))
        similarity_rating = w1.similarity(w2)
        colors["red"] = similarity_rating / songs[song][word]
        
        w1 = nlp(unicode("blue"))
        similarity_rating = w1.similarity(w2)
        colors["blue"] = similarity_rating / songs[song][word]

        w1 = nlp(unicode("indigo"))
        similarity_rating = w1.similarity(w2)
        colors["indigo"] = similarity_rating / songs[song][word]

        w1 = nlp(unicode("purple"))
        similarity_rating = w1.similarity(w2)
        colors["purple"] = similarity_rating / songs[song][word]

    colors['red'] /= word_count
    colors['orange'] /= word_count
    colors['yellow'] /= word_count
    colors['green'] /= word_count
    colors['blue'] /= word_count
    colors['indigo'] /= word_count
    colors['purple'] /= word_count

    palette['colors'] = colors

my_colors = [  palette['colors']['red']  , palette['colors']['orange'] , palette['colors']['yellow'], palette['colors']['green'] , palette['colors']['blue'], palette['colors']['indigo'],  palette['colors']['purple'] ] 

color_string = ""
my_max = max(my_colors)
for color in my_colors:
    color = int(  (color / my_max) * 9 )
    color_string += str(color) 

print(color_string)

import serial
ser = serial.Serial('/dev/ttyUSB0') # open first serial port
print(ser.name)      # check which port was really used
ser.write(str(color_string) )     # write a string
ser.close()             # close port