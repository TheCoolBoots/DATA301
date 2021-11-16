from Crypto.Util import number

def RSA_encrypt():
    pass

def RSA_decrypt():
    pass

# Source = https://algorithmist.com/wiki/Modular_inverse
# Iterative Algorithm (xgcd)
def iterative_egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q # use x//y for floor "floor division"
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = iterative_egcd(a, m) 
    if g != 1:
        return None
    else:
        return x % m

def padString(string):
    if(len(string) % 16 != 0):
        newLen = (len(string)//16 + 1) * 16
        addedBytes = newLen - len(string)
        padding = chr(newLen) * addedBytes
        return string + padding
    else:
        return string