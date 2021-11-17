
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
# p = 37
p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371

# large prime number
g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EE22B3B2E5

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

