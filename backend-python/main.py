import random
from pydantic import BaseModel
from fastapi import FastAPI

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_coprime(a, b):
    return gcd(a, b) == 1

def mod_inverse(e, phi):
    """Computes the modular inverse of e modulo phi using the extended Euclidean algorithm."""
    original_phi = phi
    x0, x1 = 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + original_phi if x1 < 0 else x1

def generate_keys(p, q):
    """Generates RSA public and private keys given two prime numbers p and q."""
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while not is_coprime(e, phi):
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(message: str, public_key):
    """Encrypts a string message using the RSA public key."""
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext: list, private_key):
    """Decrypts an RSA-encrypted message using the private key."""
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

# Initialize FastAPI app
app = FastAPI()

# Example primes
p = 61
q = 53
public_key, private_key = generate_keys(p, q)

class EncryptRequest(BaseModel):
    message: str

class DecryptRequest(BaseModel):
    ciphertext: list[int]

@app.post("/encrypt")
def encrypt_message(request: EncryptRequest):
    encrypted = encrypt(request.message, public_key)
    return {"ciphertext": encrypted}

@app.post("/decrypt")
def decrypt_message(request: DecryptRequest):
    decrypted = decrypt(request.ciphertext, private_key)
    return {"message": decrypted}
