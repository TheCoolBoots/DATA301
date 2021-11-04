import sys

def vignereCipher(inputFile, key, shift):
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

    if not key.isalpha():
        print("Key must consist of only upper and lowercase letters")
        return

    cipherText = ""

    for i, char in enumerate(inputText):
        if 65 <= ord(char) and ord(char) <= 90: # if the character is an uppercase letter
            newChar = chr((ord(char) - 65 + ord(key[i % len(key)]) - 65) % 26 + 65)
            cipherText += newChar
        elif 97 <= ord(char) and ord(char) <= 122: # if the character is a lowercase letter
            newChar = chr((ord(char) - 97 + ord(key[i % len(key)].lower) - 97) % 26 + 97)
            cipherText += newChar
        else:       # add any other characters without cipher
            cipherText += char

    print(cipherText)


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("Invalid number of arguments; python vignereCipher.py inputfile key shift")
    else:
        vignereCipher(sys.argv[1], sys.argv[2], sys.argv[3])