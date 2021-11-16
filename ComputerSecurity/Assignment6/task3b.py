import sympy # to handle prime numbers
from binascii import hexlify
import math

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

# --------------------------------
class RSA:
    def __init__(self, p=sympy.randprime(math.pow(2, 511), math.pow(2, 512)), q=sympy.randprime(math.pow(2, 511), math.pow(2, 512))):
        self.e = 65537 # a constant and a prime number!
        # phi has to be bigger than e
        # phi can't have 65537 prime factor
        self.p = p
        self.q = q
        while True:
            self.phi = (self.p - 1)*(self.q - 1)
            factors_phi = sympy.ntheory.factorint(self.phi)
            if factors_phi.get(65537, None) == None:
                # no common factor
                break
            else:
                self.p = sympy.randprime(math.pow(2, 511), math.pow(2, 512))
                self.q = sympy.randprime(math.pow(2, 511), math.pow(2, 512))
        self.n = self.p * self.q
        self.d = modinv(self.e, self.phi) # modular inversion e *d mod phi = 1
        print(self.n)
    
    def encrypt(self, message):
        # convert to hex, then to integer
        int_representation = 0
        for c in message:
            int_representation *= 1000
            int_representation += ord(c)
        print("int_representation:", int_representation)
        return pow(int_representation, self.e, self.n)

    def decrypt(self, cipher):
        message = pow(cipher, self.d, self.n)
        print("message", message)
        in_ascii = ""
        while True:
            current_num = message % 1000
            current_char = chr(current_num)
            in_ascii = current_char + in_ascii
            message = int(message/1000)
            if message < 1000:
                current_char = chr(message)
                in_ascii = current_char + in_ascii
                break
        return in_ascii

'''
Part I. Given n and e
'''

def mallory_attack_n_e(n, e):
    # find the p and q that makes n
    n_factors = sympy.ntheory.factorint(n)
    nums = list(n_factors.keys())
    phi = (nums[0] - 1) * (nums[1] -1)

    # find d
    d = modinv(e, phi)

    return phi, d

rsa = RSA()
cipher = rsa.encrypt("Hi Bob!")

print("-----mallory attack with n and e")
phi, d = mallory_attack_n_e(rsa.n, rsa.e) #given rsa.n and rsa.e because they were leaked
mallory_decrypts = pow(cipher, d, rsa.n)


'''
Part II. Given p and q
'''

def mallory_attack_p_q(p, q):
    # find the p and q that makes n
    n = p * q
    phi = (p - 1) * (q - 1)

    # brute force e and d
    for e in range(n):
        # e has to be a prime
        if not sympy.isprime(e):
            continue

        d = modinv(e, phi)
        if (e * d) % n == 1:
            return n, d

    return n, d

rsa = RSA()
cipher = rsa.encrypt("Hi Bob!")

print("-----mallory attack with p and q")
n, d = mallory_attack_n_e(rsa.p, rsa.q) #given rsa.p and rsa.q because they were leaked
mallory_decrypts = pow(cipher, d, n)

'''
Part III. Diffie-Hellman
'''

Alice_rsa = RSA()
Alice_pub = Alice_rsa.e # Alice published her public key

BOB_rsa = RSA(p=Alice_pub) #Bob rsa is public

