from Crypto.Hash import SHA256
import datetime as t
import os
import bcrypt
from nltk.corpus import words
import nltk

def task1_a():
    shaHash = SHA256.new()  
    for i in range(10):
        shaHash.update(os.urandom(16))
        print(shaHash.hexdigest())

def task1_b():
    shaHash = SHA256.new()
    for i in range(10):
        byteArray1 = os.urandom(16)
        byteArray2 = byteArray1[0:15] + bytes((byteArray1[15] ^ 1))
        print('=====================')
        shaHash.update(byteArray1)
        print(shaHash.hexdigest())
        shaHash.update(byteArray2)
        print(shaHash.hexdigest())

def task1_c(hashWidth):
    shaHash = SHA256.new()
    attemptedHashes = {}
    currentNum = 0
    startTime = t.datetime.now()

    while True:
        shaHash.update(bytes(currentNum))
        currentHash = shaHash.hexdigest()[0:hashWidth]

        if attemptedHashes[currentHash] == None:
            attemptedHashes[currentHash] = currentNum
        elif attemptedHashes[currentHash] != currentNum:
            print(f'{currentNum} and {attemptedHashes[currentHash]} both share the first {hashWidth} bytes: {currentHash}')
            break
        
        currentNum += 1

    endTime = t.datetime.now()
    print(f'Time elapsed = {endTime - startTime}')
    print(f'Number of inputs tried = {currentNum}')
    print(f'Datapoint for graph: ({hashWidth}, {endTime - startTime})')
    return hashWidth, endTime - startTime

def task1_c_generateData():
    for i in range(8, 50):
        print(f'Digest Size = {i}')
        task1_c(i)

def importUserHashes(filepath):
    with open(filepath, 'rb') as inputFile:
        contents = inputFile.readlines()
    userHashes = {}
    for user in contents:
        name = user[0:user.index(b':')]
        saltHash = user[user.index(b':') + 1:]
        userHashes[name] = {'salt':saltHash[0:29], 'hash':saltHash[29:], 'saltHash':saltHash}
    return userHashes


def task2():
    userHashes = importUserHashes('ComputerSecurity\Hashing\shadow.txt')
    nltk.download('words')
    filtered = list(filter(lambda word: len(word) >= 6 and len(word) <= 10, words.words()))
    filtered = [s.encode() for s in filtered]

    hash = bcrypt.hashpw(b"registrationsucks", b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.")
    print(bcrypt.checkpw(b'registrationsucks', hash))

    print(len(filtered))
    
    for user, saltHash in userHashes.items():
        for i, word in enumerate(filtered): 
            if(bcrypt.checkpw(word, saltHash['saltHash'])):
                print(f"{user}'s password is: {word}")
            if(i%10000 == 0):
                print(f'{i} words attempted for {user}')


task2()