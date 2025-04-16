import random
import hashlib
from rsa_core import *

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def hash_message(message: str, algo: str = "SHA-256") -> int:
    msg = message.encode()
    if algo == "SHA-256":
        return int.from_bytes(hashlib.sha256(msg).digest(), 'big')
    elif algo == "SHA-384":
        return int.from_bytes(hashlib.sha384(msg).digest(), 'big')
    elif algo == "SHA-512":
        return int.from_bytes(hashlib.sha512(msg).digest(), 'big')
    raise ValueError("Unsupported hash algorithm")

def generate_dsa_keys(L=512, N=160):
    # Step 1: Generate q
    while True:
        q = random.getrandbits(N)
        if q % 2 == 1 and is_probable_prime(q):
            break

    # Step 2: Generate p such that p-1 is multiple of q
    while True:
        k = random.getrandbits(L - N)
        p = k * q + 1
        if is_probable_prime(p):
            break

    # Step 3: Find generator g
    while True:
        h = random.randint(2, p - 2)
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
    x = random.randint(1, q - 1)  # Private key
    y = pow(g, x, p)             # Public key

    return (p, q, g, y), (x, p, q)

def dsa_sign(message: str, private_key, hash_algo="SHA-256"):
    x, p, q = private_key
    g = 2  # You can make it dynamic if needed
    h = hash_message(message, hash_algo)

    while True:
        k = random.randint(1, q - 1)
        r = pow(g, k, p) % q
        if r == 0:
            continue
        k_inv = mod_inverse(k, q)
        s = (k_inv * (h + x * r)) % q
        if s != 0:
            break

    return (r, s)

def dsa_verify(message: str, signature, public_key, hash_algo="SHA-256") -> bool:
    r, s = signature
    p, q, g, y = public_key
    if not (0 < r < q and 0 < s < q):
        return False

    h = hash_message(message, hash_algo) % q

    try:
        w = mod_inverse(s, q)
    except ZeroDivisionError:
        return False 

    u1 = (h * w) % q
    u2 = (r * w) % q

    gu1 = pow(g, u1, p)
    yu2 = pow(y, u2, p)
    v = (gu1 * yu2 % p) % q

    return v == r

