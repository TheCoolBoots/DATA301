from math import gcd
from Crypto.Util import number

def RSA_encrypt(message:str, e, n):
    byteMessage = bytearray(message, 'ascii')
    intMessage = int.from_bytes(byteMessage, "big")
    return (intMessage ** e) % n

def RSA_decrypt(ciphertext, d, n):
    intMessage = (ciphertext ** d) % n
    byteMessage = bytearray(intMessage)
    return byteMessage.decode('ascii')

def generateKeypairs(bitwidth, e):
    # choose 2 prime numbers p, q
    p = number.getPrime(bitwidth)
    q = number.getPrime(bitwidth)
    
    n = p*q

    # num coprimes with N = (p-1)(q-1) = Phi(N)
    phi = (p-1)*(q-1)

    # choose e such that 1 < e < Phi, e is coprime with N and Phi(N)
    while e < phi:
        if gcd(e, phi) == 1:
            break
        else:
            e += 1

    # choose d such that (d * e) % Phi(N) = 1
    k = 2
    d = (1 + (k*phi))//e

    # public key = (N, e)
    return (n, d)

e = 65537
keys = generateKeypairs(2048, e)

BobPrivateKey = keys[1]
n = keys[0]

AliceMessage = "Computer Security is Fun!"
AliceEncrypted = RSA_encrypt(AliceMessage, e, n)

BobDecrypted = RSA_decrypt(AliceEncrypted, BobPrivateKey, n)
print(BobDecrypted)
