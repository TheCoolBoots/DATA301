from Crypto.Cipher import AES

from Encoders.OTPEncrypt import generateRandomKey

# cipher = AES.new(key, AES.MODE_ECB)

blockSizeBytes = 16

def xorStrings(str1, str2):
    if len(str1) != len(str2):
        print("ERROR: strings are not of equal length")
        return
    
    newStr = ""
    for i in range(len(str1)):
        newStr += chr(ord(str1[i]) ^ ord(str2[i]))

    return newStr

def ECBEncrypt(key, plaintext):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return

    plaintext = padPlaintext(plaintext)

    cipherText = ""

    for i in range(0, len(plaintext)//blockSizeBytes):
        cipherText += xorStrings(plaintext[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], key)
        # print(plaintext[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes])
    
    return cipherText

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


def padPlaintext(plaintext):
    if(len(plaintext) % blockSizeBytes != 0):
        newLen = (len(plaintext)//blockSizeBytes + 1) * blockSizeBytes
        addedBytes = newLen - len(plaintext)
        paddedText = chr(addedBytes) * newLen
        paddedText = plaintext + paddedText[-addedBytes:]
        return paddedText
    else:
        return plaintext

def encryptBMP(filepath):
    key1 = generateRandomKey(blockSizeBytes)
    key2 = generateRandomKey(blockSizeBytes)
    initVector = generateRandomKey(blockSizeBytes)

    with open(filepath, 'r') as ecbOutput:
        txt = ecbOutput.read()
        header = txt[0:54]
        ecbEncryptedMessage = ECBEncrypt(key1, txt)
        ecbEncryptedMessage = header + ecbEncryptedMessage[54:]

    with open('ECB.bmp', 'w+') as file:
        file.write(ecbEncryptedMessage)

    with open(filepath, 'r') as ecbOutput:
        txt = ecbOutput.read()
        header = txt[0:54]
        ecbEncryptedMessage = CBCEncrypt(key2, initVector, txt)
        ecbEncryptedMessage = header + ecbEncryptedMessage[54:]

    with open('CBC.bmp', 'w+') as file:
        file.write(ecbEncryptedMessage)

# print(padPlaintext("ABCDEF").encode('ascii'))
# tmp = ECBEncrypt("aaaaaaaaaaaaaaaa", "b"*16+"c"*8)
# print(tmp.encode('ascii'))