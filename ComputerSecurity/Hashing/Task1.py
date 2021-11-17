from Crypto.Hash import SHA256
import datetime as t
import os
import bcrypt

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

        if currentHash not in attemptedHashes:
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

def task2():
    password = b'genius'
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print(hashed)

task2()