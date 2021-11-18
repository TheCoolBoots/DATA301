import os
import re
import math
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords

def importRawDocuments(documentFolder:str = "") -> dict:
    rawDocuments = {}
    for filename in os.listdir(documentFolder): 
        docNum = int(filename[:-4])
        with open(documentFolder + '/' + filename, 'r') as file:
            fileContents = file.read()
        fileContents = fileContents.replace('\n', ' ').replace('-',' ').replace('(',' ').replace(')',' ').replace('"','').replace(',','').replace('/', '').replace(':','').replace('.', '').replace('=', ' ')
        re.sub(r'[^A-Za-z ]', '', fileContents)
        fileContents = fileContents.split(' ')
        fileContents = list(filter(lambda string: not string.isnumeric() and len(string) > 1 and string not in stopwords.words('english'), fileContents))
        fileContents = list(map(lambda string: string.strip(), fileContents))
        rawDocuments[docNum] = fileContents
        
    return rawDocuments


def getListOfAllWords(rawDocuments:dict, rawQueries:dict) -> list:
    allWordsInDocuments = set()
    for words in rawDocuments.values():
        allWordsInDocuments.update(words)
    for words in rawQueries.values():
        allWordsInDocuments.update(words)
    return list(allWordsInDocuments)


def getWordsPerDocument(rawDocuments:dict, allWordsInDocuments:list) -> dict:
    wordCountsPerDocument = {}
    wordIndexes = {}    # instead of iterating through list to find index, just lookup in dictionary
                        # probably much more efficient

    for i, word in enumerate(allWordsInDocuments):
        wordIndexes[word] = i

    print(f'Num words = {len(allWordsInDocuments)}')
    print(f'Num documents = {len(rawDocuments)}')

    for docID, documentContent in rawDocuments.items():
        wordCounts = np.array([0] * len(allWordsInDocuments))
        for word in documentContent:
            wordCounts[wordIndexes[word]] += 1
        wordCounts = pd.Series(wordCounts, index=allWordsInDocuments)
        wordCounts.sort_values(ascending=False, inplace=True)
        wordCountsPerDocument[docID] = wordCounts
        # if(docID % 10 == 0):
        #     print(f'Current DocID = {docID}')
    return wordCountsPerDocument


def calculateTermFrequencies(documentFrame:pd.DataFrame, rawDocuments:dict, wordCountPerDocument:pd.Series) -> None:
    print('Calculating Term Frequencies')
    for docID, documentContent in rawDocuments.items():
        colName = 'TFd'+str(docID)
        documentFrame[colName] = documentFrame['terms'].apply(lambda word: documentContent.count(word)/wordCountPerDocument[docID].iloc[0])
        if(docID % 100 == 0):
            print(f'Current DocID = {docID}')


def getDocumentFrequency(wordCountPerDocument:dict, allWordsInDocuments) -> list:
    print('Calculating Document Frequencies')
    docFrequency = np.array([0] * len(allWordsInDocuments))
    for wordCount in wordCountPerDocument.values():
        docFrequency += wordCount
    return docFrequency.tolist()


def calculateTFIDF(rawDocuments:dict, documentFrame:pd.DataFrame):
    print('Calculating TFIDF')
    for docID in rawDocuments.keys():
        tfColName = 'TFd' + str(docID)
        tfidfColName = 'TFIDFd' + str(docID)
        documentFrame[tfidfColName] = documentFrame['IDF'] * documentFrame[tfColName]
        if(docID % 100 == 0):
            print(f'Current DocID = {docID}')


def generateTFIDF(documentFolder, queryFolder):
    
    rawDocuments = importRawDocuments(documentFolder)
    rawQueries = importRawDocuments(queryFolder)
    print('import done')
    allWordsInDocuments = getListOfAllWords(rawDocuments, rawQueries)
    print('allWords done')
    wordCountPerDocument = getWordsPerDocument(rawDocuments, allWordsInDocuments)
    print('wordCountPerDoc done')

    documentFrame = pd.DataFrame({'terms': allWordsInDocuments})

    calculateTermFrequencies(documentFrame, rawDocuments, wordCountPerDocument)
    print('calculatedTermFrequency')

    documentFrequency = getDocumentFrequency(wordCountPerDocument, allWordsInDocuments)
    print('calculatedDocumentFrequency')

    # print(documentFrequency[83])
    documentFrame['DF'] = documentFrequency
    documentFrame['DF'] = documentFrame['DF'].apply(lambda val: 1 if val == 0 else val)
    documentFrame['IDF'] = np.log2(len(rawDocuments.keys())/documentFrame['DF'])

    # print(list(documentFrame['IDF'].values))

    calculateTFIDF(rawDocuments, documentFrame)
    print('calculatedTFIDF')

    return documentFrame, allWordsInDocuments, wordCountPerDocument, len(rawDocuments), len(rawQueries)


def calculateQueryFrequencies(documentFrame:pd.DataFrame, rawDocuments:dict, wordCountPerDocument:pd.Series) -> None:
    for docID, documentContent in rawDocuments.items():
        colName = 'TFq'+str(docID)
        documentFrame[colName] = documentFrame['terms'].apply(lambda word: documentContent.count(word)/wordCountPerDocument[docID].iloc[0])


def calculateQueryWeights(documentFrame:pd.DataFrame, rawDocuments:dict):
    for docID in rawDocuments.keys():
        colName = 'QueryWeight' + str(docID)
        TFcol = 'TFq'+str(docID)
        documentFrame[colName] = (.5 + .5 * documentFrame[TFcol]) * documentFrame['IDF']
        # documentFrame[colName] = documentFrame[TFcol] * documentFrame['IDF']


def generateQueryTFIDF(queryFolder:str, allWordsInDocuments:list, IDF:list):
    rawQueries = importRawDocuments(queryFolder)
    wordCountPerDocument = getWordsPerDocument(rawQueries, allWordsInDocuments)
    print('calculated word count per document')

    queryFrame = pd.DataFrame({'terms': allWordsInDocuments})
    calculateQueryFrequencies(queryFrame, rawQueries, wordCountPerDocument)
    print('calculated query frequencies')

    queryFrame['IDF'] = IDF

    calculateQueryWeights(queryFrame, rawQueries)
    print('calculated query weights')

    return queryFrame

def magnitude(vector:pd.Series):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def calculateCosineSimilarity(docName:str, queryName:str, documentFrame:pd.DataFrame, queryFrame:pd.DataFrame):
    cosSimilarity = math.acos(documentFrame[docName].dot(queryFrame[queryName])/(magnitude(documentFrame[docName]) * magnitude(queryFrame[queryName])))
    return cosSimilarity

def getMostSimilarDocuments(queryNum, documentFrame, queryFrame, numDocuments):
    docNumbers = range(1, numDocuments + 1)
    similarities = []
    queryName = 'QueryWeight' + str(queryNum)

    for docNum in docNumbers:
        docName = 'TFIDFd' + str(docNum)
        similarities.append(calculateCosineSimilarity(docName, queryName, documentFrame, queryFrame))
    similaritiesFrame = pd.DataFrame({'cosSimilarity':similarities}, index=docNumbers)

    similaritiesFrame.sort_values(by='cosSimilarity', ascending=True, inplace=True)
    if(numDocuments < 20):
        return similaritiesFrame.head(numDocuments)
    else:
        return similaritiesFrame.head(20)

def getTop20Similar(documentFrame, queryFrame, numDocuments, numQueries):
    if(numQueries > 20):
        numQueries = 20

    similarList = []

    for i in range(1, numQueries+1):          # for each query starting at query 0
        similarSeries = getMostSimilarDocuments(i, documentFrame, queryFrame, numDocuments)
        # print(similarSeries)
        similarList.append(similarSeries.index)

    output = pd.Series(similarList, index = range(1, numQueries+1))
    # print(output.head(20))

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
    
    return mapping

def calcMAPScore(humanList, computerList):
    numShared = 0
    mapScore = 0
    for i, docNum in enumerate(computerList):
        if docNum in humanList:
            numShared += 1
            mapScore += numShared/(i+1)

    return mapScore/len(humanList)

def calcAllMAPScores(humanJudgement, compJudgement):
    mapScores = {}
    print(compJudgement)
    for query in compJudgement.index:
        mapScores[query] = calcMAPScore(humanJudgement[query], compJudgement[query])
    
    return pd.DataFrame({'docNum':mapScores.keys(), 'mapScore':mapScores.values()})

nltk.download('stopwords')

testDocuments = generateTFIDF('labs/lab6/documents', 'labs/lab6/queries')   # testDocuments = (documentFrame, allWordsInDocuments, wordCountPerDocument, len(rawDocuments), len(rawQueries))
testQueries = generateQueryTFIDF('labs/lab6/queries', testDocuments[1], testDocuments[0]['IDF'])
# testDocuments = generateTFIDF('labs/lab6/testFolder', 'labs/lab6/testQueries')
# testQueries = generateQueryTFIDF('labs/lab6/testQueries', testDocuments[1], testDocuments[0]['IDF'])

testDocuments[0].to_csv('documentFrame')
testQueries.to_csv('queryFrame')

noNanDocs = testDocuments[0].fillna(0)
noNanQueries = testQueries.fillna(0)


mostSimilarDocuments = getTop20Similar(noNanDocs, noNanQueries, testDocuments[3], testDocuments[4]) # pandas series where index = docnum, vals = lists of relevant documents

# print(mostSimilarDocuments)

humanSimilarDocs = getRelevantDocsPerQuery('labs/lab6/human_judgement.txt')     # dictionary mapping docNum to list of relevant Documents
# humanSimilarDocs = getRelevantDocsPerQuery('labs/lab6/humanJudgementTest')
print(humanSimilarDocs)



mapScores = calcAllMAPScores(humanSimilarDocs, mostSimilarDocuments)
print(mapScores)