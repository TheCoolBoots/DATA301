import random
from ECBencryption import xorStrings
from ECBencryption import generateRandomKey
from ECBencryption import CBCEncrypt
from ECBencryption import CBCDecrypt

numUsers = 456
numSessions = 31337
blockSizeBytes = 16

def urlEncodeString(string:str):
    string = string.replace(';', '%3B')
    string = string.replace('=', '%3D')
    return string

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

