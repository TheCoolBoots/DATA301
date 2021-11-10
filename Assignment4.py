import numpy as np
import pandas as pd
import math
d1 = 'a a b a c a'.split(' ')
d2 = 'b b a a c c a'.split(' ')
d3 = 'a c c'.split(' ')

query = 'a b'.split(' ')

allLetters = list(set(d1 + d2 + d3))

frame = pd.DataFrame({"terms" :allLetters})
frame['TFd1'] = frame['terms'].apply(lambda letter: d1.count(letter)/len(d1))
frame['TFd2'] = frame['terms'].apply(lambda letter: d2.count(letter)/len(d2))
frame['TFd3'] = frame['terms'].apply(lambda letter: d3.count(letter)/len(d3))
frame['TFd4'] = frame['terms'].apply(lambda letter: query.count(letter)/len(query))

frame['DF1'] = frame['terms'].apply(lambda letter: 1 if letter in d1 else 0)
frame['DF2'] = frame['terms'].apply(lambda letter: 1 if letter in d2 else 0)
frame['DF3'] = frame['terms'].apply(lambda letter: 1 if letter in d3 else 0)
frame['DF4'] = frame['terms'].apply(lambda letter: 1 if letter in query else 0)

frame['DF'] = frame['DF1'] + frame['DF2'] + frame['DF3'] + frame['DF4']
frame.drop(columns=['DF1', 'DF2', 'DF3', 'DF4'], inplace=True)

frame['IDF'] = np.log2(4/frame['DF'])

frame['TFIDFd1'] = frame['TFd1'] * frame['IDF']
frame['TFIDFd2'] = frame['TFd2'] * frame['IDF']
frame['TFIDFd3'] = frame['TFd3'] * frame['IDF']
frame['TFIDFquery'] = frame['TFd4'] * frame['IDF']

def magnitude(vector): 
    return math.sqrt(sum(pow(element, 2) for element in vector))

cosSimilarity = []


cosSimilarity.append(frame['TFIDFd1'].dot(frame['TFIDFquery']) / (magnitude(frame['TFIDFd1']) * magnitude(frame['TFIDFquery'])))
cosSimilarity.append(frame['TFIDFd2'].dot(frame['TFIDFquery']) / (magnitude(frame['TFIDFd2']) * magnitude(frame['TFIDFquery'])))
cosSimilarity.append(frame['TFIDFd3'].dot(frame['TFIDFquery']) / (magnitude(frame['TFIDFd3']) * magnitude(frame['TFIDFquery'])))

queryCosSimiliarity = pd.DataFrame({'document':['d1', 'd2', 'd3'],
                                    'cosSimilarity':cosSimilarity})
print(frame)
print(queryCosSimiliarity)