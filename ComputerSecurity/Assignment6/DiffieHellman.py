
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
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

# public key
p = 37

# large prime number
g = 5

# private keys
a = random.randint(0, p)
b = random.randint(0, p)

# Alice
A = (g ** a) % p

# Bob
B = (g ** b) % p

# A, B exchanged between Alice and Bob

# Alice calculates private combined key with B
sa = (B ** a) % p

# Bob calculates private combined key with A
sb = (A ** b) % p

# print(sa == sb)

aliceKeyHash = SHA256.new()
aliceKeyHash.update(sa.to_bytes(8, 'big'))

bobKeyHash = SHA256.new()
bobKeyHash.update(sb.to_bytes(8, 'big'))

# print(aliceKeyHash.hexdigest()[0:16])
# print(bobKeyHash.hexdigest()[0:16])

aliceSend = padByteArray(b'Hello There')

aliceCipher = AES.new(aliceKeyHash.hexdigest()[0:16], AES.MODE_CBC, aliceKeyHash.hexdigest()[16:32])
aliceMessage = aliceCipher.encrypt(aliceSend)

bobCipher = AES.new(bobKeyHash.hexdigest()[0:16], AES.MODE_CBC, bobKeyHash.hexdigest()[16:32])
bobRecieved = bobCipher.decrypt(aliceMessage)

print(bobRecieved)

