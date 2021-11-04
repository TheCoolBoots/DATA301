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
    for i, char in enumerate(cipherTextStr):
        if 65 <= ord(char) and ord(char) <= 90: # if the character is an uppercase letter
            newChar = ord(char) - ord(key[i % len(key)].upper())
            plainText += newChar
        elif 97 <= ord(char) and ord(char) <= 122: # if the character is a lowercase letter
            newChar = chr((ord(char) - 97 + ord(key[i % len(key)].lower) - 97) % 26 + 97)
            plainText += newChar
        else:       # add any other characters without cipher
            plainText += char

    print(plainText)
            

if __name__=="__main__":
    if len(sys.argv) == 3:
        getPotentialVignereKeys(sys.argv[1], sys.argv[2])
    else:
        print("Invalid number of arguments; python vignereKeyGuesser.py cipherText key")