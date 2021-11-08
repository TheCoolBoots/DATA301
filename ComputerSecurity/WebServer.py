import random

numUsers = 456
numSessions = 31337
blockSizeBytes = 16

def generateRandomKey(length):
    return ''.join([chr(random.randint(0, 255)) for _ in range(length)])

def xorStrings(str1, str2):
    if len(str1) != len(str2):
        print("ERROR: strings are not of equal length")
        return
    
    newStr = ""
    for i in range(len(str1)):
        newStr += chr(ord(str1[i]) ^ ord(str2[i]))

    return newStr

def urlEncodeString(string:str):
    string = string.replace(';', '%3B')
    string = string.replace('=', '%3D')
    return string


def CBCEncrypt(key, initVector, plaintext):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    if len(initVector) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return

    plaintext = padPlaintext(plaintext)
    
    cipherText = ""

    lastBlock = initVector

    for i in range(0, len(plaintext)//blockSizeBytes):
        preCipherText = xorStrings(plaintext[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], lastBlock)
        newCipherText = xorStrings(preCipherText, key)
        lastBlock = newCipherText
        cipherText += lastBlock
    
    return cipherText

def CBCDecrypt(key, initVector, cipherText):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    if len(initVector) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    
    plainText = ""

    lastBlock = initVector

    for i in range(0, len(cipherText)//blockSizeBytes):
        prePlaintext = xorStrings(cipherText[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], key)
        newPlaintext = xorStrings(prePlaintext, lastBlock)
        lastBlock = cipherText[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes]
        plainText += newPlaintext
    
    return plainText


def padPlaintext(plaintext):
    if(len(plaintext) % blockSizeBytes != 0):
        newLen = (len(plaintext)//blockSizeBytes + 1) * blockSizeBytes
        addedBytes = newLen - len(plaintext)
        paddedText = chr(addedBytes) * newLen
        paddedText = plaintext + paddedText[-addedBytes:]
        return paddedText
    else:
        return plaintext

def CDCattack(targetString, encryptedMsg, decryptedMsg):
    newStr = ""
    for i, char in enumerate(targetString):
        decChar = xorStrings(encryptedMsg[i], decryptedMsg[i+ blockSizeBytes])
        newChar = xorStrings(decChar, char)
        newStr += newChar
    return newStr + encryptedMsg[len(targetString):]

def submit(userData):
    key = generateRandomKey(blockSizeBytes)
    iv = generateRandomKey(blockSizeBytes)
    userData = urlEncodeString(userData)
    userString = "userid="+str(numUsers)+';userdata='+userData+';session-id='+str(numSessions)
    userString = padPlaintext(userString)
    cipherText = CBCEncrypt(key, iv, userString)

    return (key, iv, cipherText)

def verify(key, iv, cipherText):
    plaintext = CBCDecrypt(key, iv, cipherText)
    return ';admin=true;' in plaintext


result = submit("asdf;alksdjf;alkjfasdlfkjf")
decryptedStr = CBCDecrypt(result[0], result[1], result[2])
encryptedAttack = CDCattack(";admin=true;", result[2], decryptedStr)
print(verify(result[0], result[1], encryptedAttack))

