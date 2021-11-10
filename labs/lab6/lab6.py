import os
import re
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
        while '' in fileContents:
            fileContents
        rawDocuments[docNum] = fileContents
        
    return rawDocuments


def getListOfAllWords(rawDocuments:dict) -> list:
    allWordsInDocuments = set()
    for words in rawDocuments.values():
        allWordsInDocuments.update(words)
    return list(allWordsInDocuments)


def getWordsPerDocument(rawDocuments:dict, allWordsInDocuments:list) -> dict:
    wordCountsPerDocument = {}
    for docID, documentContent in rawDocuments.items():
        wordCounts = np.array([0] * len(allWordsInDocuments))
        for word in documentContent:
            wordCounts[allWordsInDocuments.index(word)] += 1
        wordCountsPerDocument[docID] = wordCounts
        # print(sum(wordCounts) == len(documentContent.split(' ')))
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

    return documentFrame, allWordsInDocuments, wordCountPerDocument




generateTFIDF('labs/lab6/testFolder')

    # test to see if all words are being counted
    # for wordCount in wordCountPerDocument.values():
    #     print(len(allWordsInDocuments) == len(wordCount))
    # print(wordCountPerDocument)
