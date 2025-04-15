from pydantic import BaseModel
from typing import List

class KeyGenRequest(BaseModel):
    bits: int = 512

class EncryptRequest(BaseModel):
    message: str
    public_key: List[int]

class DecryptRequest(BaseModel):
    ciphertext: List[int]
    private_key: List[int]

class SignRequest(BaseModel):
    message: str
    private_key: List[int]
    hash_algorithm: str = "SHA-256"

class VerifyRequest(BaseModel):
    message: str
    signature: str
    public_key: List[int]
    hash_algorithm: str = "SHA-256"

class ElGamalKeyGenRequest(BaseModel):
    bits: int = 256

class ElGamalEncryptRequest(BaseModel):
    message: str
    public_key: List[int]  # [p, g, y]

class ElGamalDecryptRequest(BaseModel):
    a: str
    b_list: List[str]
    private_key: List[int]

class ElGamalSignRequest(BaseModel):
    message: str
    private_key: List[int]
    hash_algorithm: str = "SHA-256"

class ElGamalVerifyRequest(BaseModel):
    message: str
    signature: List[str]       # stringified r, s
    public_key: List[int]
    hash_algorithm: str = "SHA-256"

    
class DSAKeyGenRequest(BaseModel):
    L: int = 512
    N: int = 160

class DSASignRequest(BaseModel):
    message: str
    private_key: List[int]  # [x, p, q]
    hash_algorithm: str = "SHA-256"

class DSAVerifyRequest(BaseModel):
    message: str
    signature: List[str] 
    public_key: List[str]  
    hash_algorithm: str = "SHA-256"