import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'

def decodeShift(inputFile, shift = 0):
    try:
        inputFile = open(inputFile)
        inputText = inputFile.read()
        shift = int(shift)
    except IOError:
        print("Could not find inputfile " + inputFile)
    except TypeError:
        print("Shift must be of type int")
    finally:
        inputFile.close()

    inputText.replace("\n", "")

    plainText = ""

    for char in inputText:
        if 65 <= ord(char) and ord(char) <= 90:
            newChar = alphabet[ord(char) % 65 - shift]
            plainText += newChar
        elif 97 <= ord(char) and ord(char) <= 122:
            newChar = alphabetLower[ord(char) % 97 - shift]
            plainText += newChar
        else:
            plainText += char

    print(plainText)

def decodeAll(inputFile):
    try:
        inputFile = open(inputFile)
        inputText = inputFile.read()
    except IOError:
        print("Could not find inputfile " + inputFile)
    finally:
        inputFile.close()

    inputText.replace("\n", "")

    print("shift amount: plaintext")

    for shift in range(26):
        plainText = ""
        for char in inputText:
            if 65 <= ord(char) and ord(char) <= 90:
                newChar = alphabet[ord(char) % 65 - shift]
                plainText += newChar
            elif 97 <= ord(char) and ord(char) <= 122:
                newChar = alphabetLower[ord(char) % 97 - shift]
                plainText += newChar
            else:
                plainText += char
        print(str(shift) + ": " + plainText)   

if __name__=="__main__":
    if len(sys.argv) > 3:
        print("Invalid number of arguments; python caesarCipherDecoder.py inputfile [shift]")
    elif len(sys.argv) == 2:
        decodeAll(sys.argv[1])
    else:
        decodeShift(sys.argv[1], sys.argv[2])