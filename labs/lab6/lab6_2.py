import glob
import pandas as pd
import os
import glob
import numpy as np
import nltk
from nltk.corpus import stopwords


def createDataFrame(dirName, isDocument):
    documentFiles = glob.glob(dirName+'*.txt')
    rawDocText = []
    for file in documentFiles:
        with open(file, 'r') as f:
            docName = os.path.basename(file.split('.')[0])
            rawDocText.append({'document': docName, 'lines': f.readlines()})
    df = pd.DataFrame(rawDocText)
    df['text'] = df.apply(lambda row: ' '.join(row['lines']), axis=1)
    df['words'] = df.text.str.strip().str.split('[\W]+')

    stop_words = list(stopwords.words('english'))
    result = []

    for i in range(0, len(df)):
        for word in df.iloc[i]['words']:
            if(word.lower() not in stop_words and word != ''):
                result.append((df.iloc[i]['document'], word.lower()))

    words = pd.DataFrame(result, columns=['document', 'word'])
    counts = words.groupby('document').word.value_counts().to_frame().rename(columns={'word': 'frequency'})
    maxFrequency = counts.groupby('document').max().rename(columns={'frequency': 'maxFr'})
    tf = counts.join(maxFrequency)
    if (isDocument):
        tf['tf'] = tf['frequency']/tf['maxFr']
    else:
        tf['tf'] = (0.5+0.5*tf['frequency']/tf['maxFr'])
    numDocuments = df['document'].nunique()
    docFrequency = words.groupby('word').document.nunique().to_frame().rename(columns={'document': 'df'})
    docFrequency['idf'] = np.log2(numDocuments/docFrequency['df'].values)
    result = tf.join(docFrequency)
    result['tfidf'] = result['tf']*result['idf']
    return result


