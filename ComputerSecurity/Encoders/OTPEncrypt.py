import random

def xorStrings(str1, str2):
    if len(str1) != len(str2):
        print("ERROR: strings are not of equal length")
        return
    
    newStr = ""
    for i in range(len(str1)):
        newStr += chr(ord(str1[i]) ^ ord(str2[i]))

    return newStr

def generateRandomKey(length):
    return ''.join([chr(random.randint(0, 255)) for _ in range(length)])

def encryptFile(filepath, keyFilepath, cipherFilepath):
    try:
        plainTextFile = open(filepath)
    except IOError:
        print("Could not find inputfile " + filepath)

    plainText = plainTextFile.read()
    randomKey = generateRandomKey(len(plainText))
    cipherText = xorStrings(plainText, randomKey)

    print('Key placed in ' + keyFilepath)
    print('Cipher text placed in ' + cipherFilepath)

    with open("key", "w+") as key_file:
        key_file.write(randomKey)

    with open("cipherTxt", "w+") as cipher_file:
        cipher_file.write(cipherText)
    
def encryptBMP(filepath):
    with open(filepath, mode='r') as file:
        fileContent = file.read()

    # header is 54 bytes long, need to preserve them if we are to see the encoded image
    bmpHeader = fileContent[0:54]
    randomKey = generateRandomKey(len(fileContent))
    cipherText = xorStrings(fileContent, randomKey)
    cipherText = bmpHeader + cipherText[54:]

    with open("bmpKey", "w+") as key_file:
        key_file.write(randomKey)

    with open("cipherImg.bmp", "w+") as cipher_file:
        cipher_file.write(cipherText)

    return (randomKey, cipherText, fileContent)

def decryptBMP(imgFilepath, keyFilepath):
    with open(imgFilepath, mode='r') as file:
        bmpImg = file.read()

    with open(keyFilepath, mode='r') as file:
        bmpKey = file.read()

    # header is 54 bytes long, need to preserve them if we are to see the encoded image
    bmpHeader = bmpImg[0:54]
    originalFile = xorStrings(bmpImg, bmpKey)
    originalFile = bmpHeader + originalFile[54:]

    with open('original.bmp', 'w+') as file:
        file.write(originalFile)

    return originalFile

def twoTimeEncrypt(file1, file2):
    with open(file1, mode='r') as file:
        bmpImg1 = file.read()

    with open(file2, mode='r') as file:
        bmpImg2 = file.read()

    if len(bmpImg1) != len(bmpImg2):
        print("ERROR: images are not same size")
        return
    
    randomKey = generateRandomKey(len(bmpImg1))
    header1 = bmpImg1[0:54]
    header2 = bmpImg2[0:54]

    cipher1 = xorStrings(bmpImg1, randomKey)
    cipher2 = xorStrings(bmpImg2, randomKey)
    cipher3 = xorStrings(cipher1, cipher2)

    cipher1 = header1 + cipher1[54:]
    cipher2 = header2 + cipher2[54:]
    cipher3 = header1 + cipher3[54:]

    with open("bmpKey", "w+") as key_file:
        key_file.write(randomKey)

    with open("cipherImg1.bmp", "w+") as cipher_file:
        cipher_file.write(cipher1)
    
    with open("cipherImg2.bmp", "w+") as cipher_file:
        cipher_file.write(cipher2)

    with open("cipherImg3.bmp", "w+") as cipher_file:
        cipher_file.write(cipher3)



    return(randomKey, cipher1, cipher2, cipher3)

    
    


mustangEncrypted = encryptBMP('mustang.bmp')
mustangDecrypted = decryptBMP('cipherImg.bmp', 'bmpKey')

print(mustangEncrypted[2] == mustangDecrypted)

doubleEncrypt = twoTimeEncrypt('cp-logo.bmp', 'mustang.bmp')

# str1 = "Darlin dont you go"
# str2 = "and cut your hair!"
# str3 = xorStrings(str1, str2)
# print(str3.encode('hex'))
