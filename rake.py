import re

stop_word_file = "SmartStopList.txt"

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

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
print(phrase_score)
