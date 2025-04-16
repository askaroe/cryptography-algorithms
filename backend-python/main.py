from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import random, hashlib, json, logging
from pathlib import Path
from models import * 
from rsa_core import *
from elgamal_core import *
from dsa_core import *
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_DIR / "rsa.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Directories
KEY_DIR = Path("keys")
KEY_DIR.mkdir(exist_ok=True)
SIG_DIR = Path("signatures")
SIG_DIR.mkdir(exist_ok=True)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/rsa/generate-keys")
def generate_keys(req: KeyGenRequest):
    public_key, private_key = generate_rsa_keys(req.bits)
    logging.info("Keys generated")
    return {
        "public_key": [str(public_key[0]), str(public_key[1])],
        "private_key": [str(private_key[0]), str(private_key[1])]
    }
    
@app.post("/rsa/encrypt")
def encrypt(req: EncryptRequest):
    result = rsa_encrypt(req.message, tuple(req.public_key))
    result_str = [str(x) for x in result]  # <-- Convert each int to string
    logging.info("Message encrypted")
    return {"ciphertext": result_str}

@app.post("/rsa/decrypt")
def decrypt(req: DecryptRequest):
    result = rsa_decrypt(req.ciphertext, tuple(req.private_key))
    logging.info("Message decrypted")
    return {"message": str(result)}

@app.post("/rsa/sign")
def sign(req: SignRequest):
    sig = rsa_sign(req.message, tuple(req.private_key), req.hash_algorithm)
    logging.info("Message signed")
    return {"signature": str(sig)}  # return as string to preserve precision

@app.post("/rsa/verify")
def verify(req: VerifyRequest):
    sig_int = int(req.signature)  # convert back to int
    valid = rsa_verify(req.message, sig_int, tuple(req.public_key), req.hash_algorithm)
    logging.info("Signature verified: %s", "valid" if valid else "invalid")
    return {"valid": valid}

@app.post("/save-keys")
def save_keys(public_key: List[int], private_key: List[int]):
    with open(KEY_DIR / "rsa_keys.json", "w") as f:
        json.dump({"public_key": public_key, "private_key": private_key}, f)
    logging.info("Keys saved to file")
    return {"status": "saved"}

@app.post("/save-signature")
def save_signature(signature: int):
    with open(SIG_DIR / "signature.json", "w") as f:
        json.dump({"signature": signature}, f)
    logging.info("Signature saved to file")
    return {"status": "saved"}


@app.post("/elgamal/generate-keys")
def generate_keys(req: ElGamalKeyGenRequest):
    pub, priv = generate_elgamal_keys(req.bits)
    return {
        "public_key": [str(pub[0]), str(pub[1]), str(pub[2])],
        "private_key": [str(priv[0]), str(priv[1])]
    }

@app.post("/elgamal/encrypt")
def encrypt(req: ElGamalEncryptRequest):
    if len(req.public_key) != 3:
        raise HTTPException(status_code=400, detail="Public key must be [p, g, y]")
    
    # Convert public key to integers
    p, g, y = map(int, req.public_key)
    a, b_list = elgamal_encrypt(req.message, (p, g, y))

    # Convert large integers to string to avoid scientific notation
    return {
        "a": str(a),
        "b_list": [str(b) for b in b_list]
    }


@app.post("/elgamal/decrypt")
def decrypt(req: ElGamalDecryptRequest):
    a = int(req.a)
    b_list = [int(b) for b in req.b_list]
    message = elgamal_decrypt(a, b_list, tuple(req.private_key))
    return {"message": message}

@app.post("/elgamal/sign")
def sign(req: ElGamalSignRequest):
    r, s = elgamal_sign(req.message, tuple(req.private_key), req.hash_algorithm)
    return {
        "signature": [str(r), str(s)]
    }

@app.post("/elgamal/verify")
def verify(req: ElGamalVerifyRequest):
    r, s = map(int, req.signature)
    valid = elgamal_verify(
        req.message,
        (r, s),
        tuple(req.public_key),
        req.hash_algorithm
    )
    return {"valid": valid}


@app.post("/dsa/generate-keys")
def generate_keys(req: DSAKeyGenRequest):
    pub, priv = generate_dsa_keys(req.L, req.N)
    return {
    "public_key": [str(x) for x in pub],
    "private_key": [str(x) for x in priv]
}

@app.post("/dsa/sign")
def sign(req: DSASignRequest):
    signature = dsa_sign(req.message, tuple(req.private_key), req.hash_algorithm)
    r, s = signature
    return {"signature": [str(r), str(s)]}

@app.post("/dsa/verify")
def verify(req: DSAVerifyRequest):
    signature = tuple(int(x) for x in req.signature)
    public_key = tuple(int(x) for x in req.public_key)
    is_valid = dsa_verify(req.message, signature, public_key, req.hash_algorithm)

    return {"valid": is_valid}