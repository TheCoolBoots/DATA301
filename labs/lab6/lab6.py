import os
import re
import math
import pandas as pd
import numpy as np

def importRawDocuments(documentFolder:str = "") -> dict:
    rawDocuments = {}
    for filename in os.listdir(documentFolder): 
        docNum = int(filename[:-4])
        with open(documentFolder + '/' + filename, 'r') as file:
            fileContents = file.read()
        fileContents = fileContents.replace('\n', ' ')
        fileContents = fileContents.replace('.', '')
        fileContents = fileContents.replace(',', '')
        re.sub(r'[^A-Za-z ]', '', fileContents)
        fileContents = fileContents.split(' ')
        rawDocuments[docNum] = fileContents
        
    return rawDocuments


def getListOfAllWords(rawDocuments:dict) -> list:
    allWordsInDocuments = set()
    for words in rawDocuments.values():
        allWordsInDocuments.update(words)
    return list(allWordsInDocuments)


def getWordsPerDocument(rawDocuments:dict, allWordsInDocuments:list) -> dict:
    wordCountsPerDocument = {}
    wordIndexes = {}    # instead of iterating through list to find index, just lookup in dictionary
                        # probably much more efficient

    for i, word in enumerate(allWordsInDocuments):
        wordIndexes[word] = i

    for docID, documentContent in rawDocuments.items():
        wordCounts = np.array([0] * len(allWordsInDocuments))
        for word in documentContent:
            wordCounts[wordIndexes[word]] += 1
        wordCountsPerDocument[docID] = wordCounts
    return wordCountsPerDocument


def calculateTermFrequencies(documentFrame:pd.DataFrame, rawDocuments:dict, wordCountPerDocument:dict) -> None:
    for docID, documentContent in rawDocuments.items():
        colName = 'TFd'+str(docID)
        documentFrame[colName] = documentFrame['terms'].apply(lambda word: documentContent.count(word)/max(wordCountPerDocument[docID]))


def getDocumentFrequency(wordCountPerDocument:dict, allWordsInDocuments) -> list:
    docFrequency = np.array([0] * len(allWordsInDocuments))
    for wordCount in wordCountPerDocument.values():
        docFrequency += wordCount
    return docFrequency.tolist()


def calculateTFIDF(rawDocuments:dict, documentFrame:pd.DataFrame):
    for docID in rawDocuments.keys():
        tfColName = 'TFd' + str(docID)
        tfidfColName = 'TFIDFd' + str(docID)
        documentFrame[tfidfColName] = documentFrame['IDF'] * documentFrame[tfColName]


def generateTFIDF(documentFolder):
    rawDocuments = importRawDocuments(documentFolder)
    allWordsInDocuments = getListOfAllWords(rawDocuments)
    wordCountPerDocument = getWordsPerDocument(rawDocuments, allWordsInDocuments)

    documentFrame = pd.DataFrame({'terms': allWordsInDocuments})

    calculateTermFrequencies(documentFrame, rawDocuments, wordCountPerDocument)

    documentFrequency = getDocumentFrequency(wordCountPerDocument, allWordsInDocuments)

    documentFrame['DF'] = documentFrequency
    documentFrame['IDF'] = np.log2(len(rawDocuments.keys())/documentFrame['DF'])

    calculateTFIDF(rawDocuments, documentFrame)

    return documentFrame, allWordsInDocuments, wordCountPerDocument, len(rawDocuments)


def calculateQueryFrequencies(documentFrame:pd.DataFrame, rawDocuments:dict, wordCountPerDocument:dict) -> None:
    for docID, documentContent in rawDocuments.items():
        colName = 'TFq'+str(docID)
        documentFrame[colName] = documentFrame['terms'].apply(lambda word: documentContent.count(word)/max(wordCountPerDocument[docID]))


def calculateQueryWeights(documentFrame:pd.DataFrame, rawDocuments:dict):
    for docID in rawDocuments.keys():
        colName = 'QueryWeight' + str(docID)
        TFcol = 'TFq'+str(docID)
        # documentFrame[colName] = (.5 + .5 * documentFrame[TFcol]) * documentFrame['IDF']
        documentFrame[colName] = documentFrame[TFcol] * documentFrame['IDF']


def generateQueryTFIDF(documentFolder:str, allWordsInDocuments:list, IDF:list):
    rawDocuments = importRawDocuments(documentFolder)
    wordCountPerDocument = getWordsPerDocument(rawDocuments, allWordsInDocuments)

    documentFrame = pd.DataFrame({'terms': allWordsInDocuments})
    calculateQueryFrequencies(documentFrame, rawDocuments, wordCountPerDocument)

    documentFrame['IDF'] = IDF

    calculateQueryWeights(documentFrame, rawDocuments)

    return documentFrame

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def calculateCosineSimilarity(docName:str, queryName:str, documentFrame:pd.DataFrame, queryFrame:pd.DataFrame):
    return math.acos(documentFrame[docName].dot(queryFrame[queryName])/(magnitude(documentFrame[docName]) * magnitude(queryFrame[queryName])))
    # return documentFrame[docName].dot(queryFrame[queryName])/(magnitude(documentFrame[docName]) * magnitude(queryFrame[queryName]))

def getMostSimilarDocuments(queryNum, documentFrame, queryFrame, numDocuments):
    docNumbers = range(1, numDocuments+1)
    similarities = []
    for docNum in docNumbers:
        docName = 'TFIDFd' + str(docNum)
        queryName = 'QueryWeight' + str(queryNum)
        similarities.append(calculateCosineSimilarity(docName, queryName, documentFrame, queryFrame))
    similaritiesFrame = pd.DataFrame({'cosSimilarity':similarities}, index=docNumbers)
    # similaritiesFrame.sort_values(by='cosSimilarity', ascending=False, inplace=True)
    similaritiesFrame.sort_values(by='cosSimilarity', ascending=True, inplace=True)
    if(numDocuments < 20):
        return similaritiesFrame.iloc[0:numDocuments]
    else:
        return similaritiesFrame.iloc[0:20]

def getTop20Similar(documentFrame, queryFrame, numDocuments):
    if len(queryFrame < 20):
        numQueries = len(queryFrame)
    else:
        numQueries = 20

    similarList = []

    for i in range(0, numQueries):
        similarSeries = getMostSimilarDocuments(i, documentFrame, queryFrame, numDocuments)
        similarList.append(similarSeries.index)

    output = pd.Series(similarList, index = range(0, numQueries))

    return output

def getRelevantDocsPerQuery(judgementFile):
    data = pd.read_csv(judgementFile,sep=' ')
    data.drop(columns='empty', inplace=True)
    data = data[data['relevance'] < 4]
    data = data[data['relevance'] > 0]

    mapping = {}
    for query in data['queryNum'].drop_duplicates():
        mapping[query] = []

    for i in range(0, len(data.index)):
        mapping[data.iloc[i]['queryNum']].append(data.iloc[i]['docNum'])

    print(mapping)
    
    return mapping

def calcMAPScore(humanList, computerList):
    numShared = 0
    mapScore = 0
    for i, docNum in enumerate(computerList):
        if docNum in humanList:
            numShared += 1
        mapScore += numShared/i

    return mapScore/len(humanList)

def calcAllMAPScores(humanJudgement, compJudgement):
    mapScores = {}
    for query in compJudgement.index:
        mapScores[query] = calcMAPScore(humanJudgement[query], compJudgement[query])
    
    return pd.DataFrame({'docNum':mapScores.keys(), 'mapScore':mapScores.values()})



testDocuments = generateTFIDF('labs/lab6/documents')
testQueries = generateQueryTFIDF('labs/lab6/queries', testDocuments[1], testDocuments[0]['IDF'])

print(testDocuments[0])
print(testQueries)

print(getMostSimilarDocuments(1, testDocuments[0], testQueries, 5))

mostSimilarDocuments = getTop20Similar(testDocuments[0], testQueries, testDocuments[3])

# print(mostSimilarDocuments)

# test to see if all words are being counted
# for wordCount in wordCountPerDocument.values():
#     print(len(allWordsInDocuments) == len(wordCount))
# print(wordCountPerDocument)

humanSimilarDocs = getRelevantDocsPerQuery('labs/lab6/human_judgement.txt')

mapScores = calcAllMAPScores(humanSimilarDocs, mostSimilarDocuments)
print(mapScores)