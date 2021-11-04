import sys
def caesarCipher(inputFile, shift):
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

    cipherText = ""

    for char in inputText:
        if 65 <= ord(char) and ord(char) <= 90:
            newChar = chr(((ord(char) + shift) - 65) % 26 + 65)
            cipherText += newChar
        elif 97 <= ord(char) and ord(char) <= 122:
            newChar = chr(((ord(char) + shift) - 97) % 26 + 97)
            cipherText += newChar
        else:
            cipherText += char

    print(cipherText)

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Invalid number of arguments; python caesarCipher.py inputfile shift")
    else:
        caesarCipher(sys.argv[1], sys.argv[2])