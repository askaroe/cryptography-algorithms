import random
import hashlib
from typing import Tuple

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
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  # Ensure it's odd and has the right bit length
        if is_probable_prime(p):
            return p

def is_probable_prime(n, k=5):
    if n <= 1 or n % 2 == 0:
        return False
    if n == 2 or n == 3:
        return True

    # write n - 1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x in (1, n - 1):
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def hash_message(message: str, algo: str = "SHA-256") -> int:
    m = message.encode()
    if algo == "SHA-256":
        return int.from_bytes(hashlib.sha256(m).digest(), 'big')
    elif algo == "SHA-384":
        return int.from_bytes(hashlib.sha384(m).digest(), 'big')
    elif algo == "SHA-512":
        return int.from_bytes(hashlib.sha512(m).digest(), 'big')
    raise ValueError("Unsupported hash algorithm")

def generate_elgamal_keys(bits=512) -> Tuple[Tuple[int, int, int], Tuple[int, int]]:
    p = generate_large_prime(bits)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)  # private key
    g = 2
    y = pow(g, x, p)  # public key
    public_key = (p, g, y)
    private_key = (x, p)
    return public_key, private_key

def elgamal_encrypt(message: str, public_key: Tuple[int, int, int]):
    p, g, y = public_key
    m = [ord(c) for c in message]
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b_list = [(pow(y, k, p) * val) % p for val in m]
    return a, b_list

def elgamal_decrypt(a: int, b_list: list[int], private_key: Tuple[int, int]):
    x, p = private_key
    s = pow(a, x, p)
    s_inv = mod_inverse(s, p)
    m = [(b * s_inv) % p for b in b_list]
    return ''.join(chr(val) for val in m)

def elgamal_sign(message: str, private_key: Tuple[int, int], hash_algo="SHA-256"):
    x, p = private_key
    g = 2  # should match the g used during key generation
    h = hash_message(message, hash_algo) % (p - 1)  # reduce hash mod (p - 1)

    while True:
        k = random.randint(2, p - 2)
        if gcd(k, p - 1) == 1:
            break

    r = pow(g, k, p)
    k_inv = mod_inverse(k, p - 1)
    s = (k_inv * ((h - x * r) % (p - 1))) % (p - 1)
    
    return (r, s)


def elgamal_verify(message: str, signature: Tuple[int, int], public_key: Tuple[int, int, int], hash_algo="SHA-256"):
    p, g, y = public_key
    r, s = signature

    g = 2
    
    if not (0 < r < p) or not (0 < s < p):
        return False

    h = hash_message(message, hash_algo) % (p - 1)

    v1 = (pow(y, r, p) * pow(r, s, p)) % p
    v2 = pow(g, h, p)

    return v1 == v2

