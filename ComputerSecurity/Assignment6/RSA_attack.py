import random
import os
from math import gcd
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import number

def RSA_encrypt(message:str, e, n):
    byteMessage = bytearray(message, 'ascii')
    # print(byteMessage)
    intMessage = int.from_bytes(byteMessage, "big")
    # print(hex(intMessage))
    return pow(intMessage, e) % n

def multiplicativeInverse(x, p):
    return pow(x, -1, p)

def RSA_decrypt(ciphertext:int, d, n):
    print(ciphertext)
    messageInt = pow(ciphertext, d) % n
    print(hex(messageInt))
    bytetext = messageInt.to_bytes(ciphertext.bit_length()//8 + 1, 'big')
    # print(bytetext)
    # print(bytetext.decode('ascii'))
    return bytetext.decode('ascii')

def generateKeypairs(bitwidth, e):
    # choose 2 prime numbers p, q
    p = number.getPrime(bitwidth)
    q = number.getPrime(bitwidth)
    
    n = p*q

    # num coprimes with N = (p-1)(q-1) = Phi(N)
    phi = (p-1)*(q-1)

    # choose d such that (d * e) % Phi(N) = 1
    k = 2
    d = (1 + (k*phi))//e    

    # public key = (N, e)
    return (n, d)

def AES_Encrypt(msg, key, iv):
    _AES = AES.new(key, AES.MODE_CBC, IV=iv)
    cipher = _AES.encrypt(msg)
    return cipher

def AES_Decrypt(cipher, key, iv):
    _AES = AES.new(key, AES.MODE_CBC, IV=iv)
    msg = _AES.decrypt(cipher)
    return msg

def padString(array):
    if(len(array) % 16 != 0):
        newLen = (len(array)//16 + 1) * 16
        addedBytes = newLen - len(array)
        padding = chr(newLen) * addedBytes
        print(padding)
        print(array)
        return array + padding
    else:
        return array

def hack(cipherText):
    return 1

e = 3

n, d = generateKeypairs(8, e)

BobMessage = str(random.randint(1, n))
c = RSA_encrypt(BobMessage, e, n)

cPrime = hack(c)    # what does this need to be such that mallory can decrypt encryptedMessage
                    # would need initVector and aliceDecrypted
                    # knows n, e, c, message
                    # doesn't know d

aliceDecrypted = RSA_decrypt(cPrime, d, n)
aliceSHA256 = SHA256.new()
aliceSHA256.update(bytearray(aliceDecrypted, 'ascii'))

initVector = os.urandom(16)
encryptedMessage = AES_Encrypt(padString("Hi Bob!"), aliceSHA256.hexdigest()[0:16], initVector)

malloryKey = RSA_decrypt(1, 1, n)
mallorySHA256 = SHA256.new()
mallorySHA256.update(bytearray(malloryKey, 'ascii'))

decryptedMessage = AES_Decrypt(encryptedMessage, mallorySHA256.hexdigest()[0:16], initVector)
print(decryptedMessage)
