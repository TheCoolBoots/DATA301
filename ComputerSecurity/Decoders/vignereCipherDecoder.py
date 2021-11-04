import sys
import pandas as pd
import numpy as np

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'

def getPotentialVignereKeys(cipherText, key):
    try:
        cipherTextFile = open(cipherText)
        cipherTextStr = cipherTextFile.read()
    except IOError:
        print("Could not find specified file: " + cipherText)
        return
    finally:
        cipherTextFile.close()

    plainText = ""
    for i in range(len(cipherTextStr)):
        if 65 <= ord(cipherTextStr[i]) and ord(cipherTextStr[i]) <= 90:
            plainText += alphabet[ord(cipherTextStr[i]) - ord(key[i % len(key)])]
        elif 97 <= ord(cipherTextStr[i]) and ord(cipherTextStr[i]) <= 122:
            plainText += alphabetLower[ord(cipherTextStr[i]) - ord(key[i % len(key)]) - 32]
        else:
            plainText += cipherTextStr[i]

    print(plainText)
            

if __name__=="__main__":
    if len(sys.argv) == 3:
        getPotentialVignereKeys(sys.argv[1], sys.argv[2])
    else:
        print("Invalid number of arguments; python vignereKeyGuesser.py cipherText key")