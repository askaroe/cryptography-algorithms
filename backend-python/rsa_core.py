import random, hashlib, json, logging
from typing import List

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    original_phi = phi
    x0, x1 = 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + original_phi if x1 < 0 else x1

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def generate_large_prime(bits=512):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # ensure it's odd and bit length
        if is_probable_prime(num):
            return num

def generate_rsa_keys(bits=512):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(message: str, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(cipher: List[int], private_key):
    d, n = private_key
    return ''.join(chr(pow(c, d, n)) for c in cipher)

def hash_message(message: str, algo: str = "SHA-256") -> int:
    msg = message.encode()
    if algo == "SHA-256":
        return int.from_bytes(hashlib.sha256(msg).digest(), 'big')
    elif algo == "SHA-384":
        return int.from_bytes(hashlib.sha384(msg).digest(), 'big')
    elif algo == "SHA-512":
        return int.from_bytes(hashlib.sha512(msg).digest(), 'big')
    raise ValueError("Unsupported hash algorithm")

def rsa_sign(message: str, private_key, algo="SHA-256"):
    d, n = private_key
    hashed = hash_message(message, algo)
    return pow(hashed, d, n)

def rsa_verify(message: str, signature: int, public_key, algo="SHA-256"):
    e, n = public_key
    hashed = hash_message(message, algo)
    return hashed == pow(signature, e, n)

def is_probable_prime(n, k=5):
    if n <= 1 or n % 2 == 0:
        return False
    if n == 2 or n == 3:
        return True

    # Write n - 1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):  # number of rounds
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
