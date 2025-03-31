import random
import os
import json
from fastapi import HTTPException

KEYS_DIR = "keys/"
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_coprime(a, b):
    return gcd(a, b) == 1

def mod_inverse(e, phi):
    original_phi = phi
    x0, x1 = 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + original_phi if x1 < 0 else x1

def generate_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while not is_coprime(e, phi):
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    public_key = {"e": e, "n": n}
    private_key = {"d": d, "n": n}

    with open(KEYS_DIR + "public_key.json", "w") as f:
        json.dump(public_key, f)

    with open(KEYS_DIR + "private_key.json", "w") as f:
        json.dump(private_key, f)

    return public_key, private_key

def encrypt(message: str, public_key):
    e, n = public_key["e"], public_key["n"]
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext: list, private_key):
    d, n = private_key["d"], private_key["n"]
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)
