import numpy as np
import pandas as pd
import math
d1 = 'a a b a c a'.split(' ')
d2 = 'b b a a c c a'.split(' ')
d3 = 'a c c'.split(' ')

query = 'a b'.split(' ')

termFrequency = {"d1" : [4, 1, 1],
                        "d2" : [3, 2, 2],
                        "d3" : [1, 0, 2],
                        "d4" : [1, 1, 0]}

allLetters = list(set(d1 + d2 + d3))

frame = pd.DataFrame({"terms" :allLetters})
frame['TFd1'] = frame['terms'].apply(lambda letter: d1.count(letter)/max(termFrequency['d1']))
frame['TFd2'] = frame['terms'].apply(lambda letter: d2.count(letter)/max(termFrequency['d2']))
frame['TFd3'] = frame['terms'].apply(lambda letter: d3.count(letter)/max(termFrequency['d3']))
frame['TFquery'] = frame['terms'].apply(lambda letter: query.count(letter)/max(termFrequency['d4']))

frame['DF1'] = frame['terms'].apply(lambda letter: 1 if letter in d1 else 0)
frame['DF2'] = frame['terms'].apply(lambda letter: 1 if letter in d2 else 0)
frame['DF3'] = frame['terms'].apply(lambda letter: 1 if letter in d3 else 0)

frame['DF'] = frame['DF1'] + frame['DF2'] + frame['DF3']
frame.drop(columns=['DF1', 'DF2', 'DF3'], inplace=True)

frame['IDF'] = np.log2(3/frame['DF']) # shouldn’t include query in documents

frame['TFIDFd1'] = frame['TFd1'] * frame['IDF']
frame['TFIDFd2'] = frame['TFd2'] * frame['IDF']
frame['TFIDFd3'] = frame['TFd3'] * frame['IDF']

frame['QueryWeight'] = (.5 + .5*frame['TFquery']) * frame['IDF']
 
def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

cosSimilarity = []

cosSimilarity.append(frame['TFIDFd1'].dot(frame['QueryWeight']) / (magnitude(frame['TFIDFd1']) * magnitude(frame['QueryWeight'])))
cosSimilarity.append(frame['TFIDFd2'].dot(frame['QueryWeight']) / (magnitude(frame['TFIDFd2']) * magnitude(frame['QueryWeight'])))
cosSimilarity.append(frame['TFIDFd3'].dot(frame['QueryWeight']) / (magnitude(frame['TFIDFd3']) * magnitude(frame['QueryWeight'])))

queryCosSimiliarity = pd.DataFrame({'document':['d1', 'd2', 'd3'],
                                    'cosSimilarity':cosSimilarity})
print(frame)
print(queryCosSimiliarity)