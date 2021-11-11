import random

blockSizeBytes = 16

def padByteArray(array):
    if(len(array) % blockSizeBytes != 0):
        newLen = (len(array)//blockSizeBytes + 1) * blockSizeBytes
        addedBytes = newLen - len(array)
        padding = bytearray(addedBytes.to_bytes(1, 'little')) * addedBytes
        # print(padding)
        # print(array)
        return array + padding
    else:
        return array

def generateRandomByteKey(length):
    return [random.randint(0, 255) for _ in range(length)]

def xorByteArray(arr1, arr2):
    if len(arr1) != len(arr2):
        print("ERROR: arrays are not of equal length")
        return
    newArray = bytearray()
    for i in range(len(arr1)):
        newArray.append(arr1[i] ^ arr2[i])
    return newArray

def ECBEncryptBinary(key, plaintext):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return

    plaintext = padByteArray(plaintext)

    cipherText = bytearray()

    for i in range(0, len(plaintext)//blockSizeBytes):
        cipherText += xorByteArray(plaintext[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], key)
    
    return cipherText

def CBCEncryptBinary(key, initVector, plaintext):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    if len(initVector) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return

    # print(plaintext)
    plaintext = padByteArray(plaintext)
    
    cipherText = bytearray()

    lastBlock = initVector

    for i in range(0, len(plaintext)//blockSizeBytes):
        preCipherText = xorByteArray(plaintext[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], lastBlock)
        newCipherText = xorByteArray(preCipherText, key)
        lastBlock = newCipherText
        cipherText += lastBlock
    
    return cipherText

def ECBDecryptBinary(key, cipherText):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    
    plaintext = bytearray()

    for i in range(0, len(cipherText)//blockSizeBytes):
        plaintext += xorByteArray(cipherText[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], key)

    return plaintext

def CBCDecryptBinary(key, initVector, cipherText):
    if len(key) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    if len(initVector) != blockSizeBytes:
        print("ERROR: key is not of length " + blockSizeBytes)
        return
    
    plainText = bytearray()

    lastBlock = initVector

    for i in range(0, len(cipherText)//blockSizeBytes):
        prePlaintext = xorByteArray(cipherText[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes], key)
        newPlaintext = xorByteArray(prePlaintext, lastBlock)
        lastBlock = cipherText[i*blockSizeBytes: i*blockSizeBytes+blockSizeBytes]
        plainText += newPlaintext
    
    return plainText

def encryptBMP(filepath):
    key1 = generateRandomByteKey(blockSizeBytes)
    key2 = generateRandomByteKey(blockSizeBytes)
    initVector = generateRandomByteKey(blockSizeBytes)

    with open(filepath, 'rb') as ecbInput:
        txt = bytearray(ecbInput.read())
    
    # print(txt)
    header = txt[0:54]
    ecbEncryptedMessage = ECBEncryptBinary(key1, txt)
    ecbEncryptedMessage = header + ecbEncryptedMessage[54:]

    with open('ECB.bmp', 'wb+') as file:
        file.write(ecbEncryptedMessage)
    
    # print(txt)
    header = txt[0:54]
    cbcEncryptedMessage = CBCEncryptBinary(key2, initVector, txt)
    cbcEncryptedMessage = header + cbcEncryptedMessage[54:]

    with open('CBC.bmp', 'wb+') as file:
        file.write(cbcEncryptedMessage)

def encryptFile(filepath):
    key1 = generateRandomByteKey(blockSizeBytes)
    key2 = generateRandomByteKey(blockSizeBytes)
    initVector = generateRandomByteKey(blockSizeBytes)

    with open(filepath, 'rb') as ecbInput:
        txt = bytearray(ecbInput.read())
    
    ecbEncryptedMessage = ECBEncryptBinary(key1, txt)
    with open('ECB', 'wb+') as file:
        file.write(ecbEncryptedMessage)

    cbcEncryptedMessage = CBCEncryptBinary(key2, initVector, txt)
    with open('CBC', 'wb+') as file:
        file.write(cbcEncryptedMessage)

    ecbDecryptedMessage = ECBDecryptBinary(key1, ecbEncryptedMessage)
    cbcDecryptedMessage = CBCDecryptBinary(key2, initVector, cbcEncryptedMessage)

    print(ecbDecryptedMessage == txt)
    print(cbcDecryptedMessage == txt)


# encryptFile('testInput')
# encryptBMP('cp-logo.bmp')

# print(padPlaintext("ABCDEF").encode('ascii'))
# tmp = ECBEncrypt("aaaaaaaaaaaaaaaa", "b"*16+"c"*8)
# print(tmp.encode('ascii'))