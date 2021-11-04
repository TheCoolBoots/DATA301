import sys
import pandas as pd
import re

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
            potentialKey = []
            
            for j in range(0, i):
                # print(str(j) + "=============")
                rawString = re.sub(r'\W+', '', cipherTextStr[j::i])

                vals = pd.Series(list(rawString))
                valCount = vals.value_counts()
                maxFrequencies = "".join(list(valCount.index[0:3]))
                
                # print(cipherTextStr[j::i])
                # print(maxFrequency)

                # take every ith term
                # count how many of each letter there is
                # assume the highest frequency letter is E
                # potentialKey[j] = alphabet[ord(hFreq) - 4]
                # potentialKey += alphabet[ord(maxFrequency.upper()) % 65 - 4]
                potentialKey.append(maxFrequencies)
            
            potentialKeys.append(potentialKey)
    else:
        potentialKey = []
            
        for j in range(0, keyLen):
            rawString = re.sub(r'\W+', '', cipherTextStr[j::keyLen])

            vals = pd.Series(list(rawString))
            valCount = vals.value_counts()
            print(valCount)
            maxFrequencies = "".join(list(valCount.index[0:3]))
            
            potentialKey.append(maxFrequencies)
        
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