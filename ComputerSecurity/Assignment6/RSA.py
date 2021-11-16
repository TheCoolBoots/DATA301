from Crypto.Util import number
from math import gcd

def RSA_encrypt(message:str, e, n):
    byteMessage = bytearray(message, 'ascii')
    intMessage = int.from_bytes(byteMessage, "big")
    return pow(intMessage, e, n)

def RSA_decrypt(ciphertext:int, d, n):
    print(ciphertext)
    messageInt = pow(ciphertext, d) % n
    print(hex(messageInt))
    bytetext = messageInt.to_bytes(ciphertext.bit_length()//8 + 1, 'big')
    # print(bytetext)
    # print(bytetext.decode('ascii'))
    return bytetext.decode('ascii')

def multiplicative_inverse(a, m):
    g, x, y = gcd(a, m)
    return x % m

def generateKeypairs(bitwidth, e):
    # choose 2 prime numbers p, q
    p = number.getPrime(bitwidth)
    q = number.getPrime(bitwidth)
    
    n = p*q

    # num coprimes with N = (p-1)(q-1) = Phi(N)
    phi = (p-1)*(q-1)

    # choose d such that (d * e) % Phi(N) = 1
    inverse = multiplicative_inverse(e, phi)
    d = pow(inverse, 1, phi)

    # public key = (N, e)
    return (n, d)

e = 65537

BobPrivateKey, n = generateKeypairs(2048, e)

AliceMessage = "YY"
AliceEncrypted = RSA_encrypt(AliceMessage, e, n)

BobDecrypted = RSA_decrypt(AliceEncrypted, BobPrivateKey, n)
print(BobDecrypted)
