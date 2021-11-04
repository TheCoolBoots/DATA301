import sys
import pandas as pd
import numpy as np

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'

def getPotentialVignereKeys(cipherText, maxKeyLength, keyLength = None):
    maxKeyLen = 0
    keyLen = None

    try:
        cipherTextFile = open(cipherText)
        cipherTextStr = cipherTextFile.read()

        maxKeyLen = int(maxKeyLength)
        if(keyLength != None):
            keyLen = int(keyLength)

    except IOError:
        print("Could not find specified file: " + cipherText)
        return
    except TypeError:
        print("maxKeyLength and keyLength must be of type integer")
        return
    finally:
        cipherTextFile.close()

    potentialKeys = []
    cipherTextStr = cipherTextStr.replace("\n", "")
    cipherTextStr = cipherTextStr.upper()

    if keyLen == None:
        for i in range(2, maxKeyLen + 1):
            potentialKey = ""
            
            for j in range(0, i):
                # print(str(j) + "=============")
                vals = pd.Series(list(cipherTextStr[j::i]))
                valCount = vals.value_counts()
                maxFrequency = valCount.index[0]
                
                # print(cipherTextStr[j::i])
                # print(maxFrequency)

                # take every ith term
                # count how many of each letter there is
                # assume the highest frequency letter is E
                # potentialKey[j] = alphabet[ord(hFreq) - 4]

                potentialKey += alphabet[ord(maxFrequency) % 65 - 4]
            
            potentialKeys.append(potentialKey)
    
    print(potentialKeys)
    return potentialKeys

if __name__=="__main__":
    if len(sys.argv) == 3:
        getPotentialVignereKeys(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        getPotentialVignereKeys(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Invalid number of arguments; python vignereKeyGuesser.py cipherText maxKeyLength [keylength]")