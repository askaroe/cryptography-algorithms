from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from rsa_utils import generate_keys, encrypt, decrypt
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Directories for saving files
KEYS_DIR = Path("keys/")
ENCRYPTED_DIR = Path("encrypted/")
DECRYPTED_DIR = Path("decrypted/")

for directory in [KEYS_DIR, ENCRYPTED_DIR, DECRYPTED_DIR]:
    directory.mkdir(exist_ok=True)


def int_list_to_ascii_string(int_list):
    """Convert list of integers to an ASCII string."""
    return "".join(chr(i) for i in int_list)


def ascii_string_to_int_list(text):
    """Convert ASCII string to a list of integers."""
    return [ord(c) for c in text]


@app.post("/generate-keys")
def generate_keys_endpoint():
    public_key, private_key = generate_keys()
    return {"public_key": json.dumps(public_key), "private_key": json.dumps(private_key)}

class EncryptRequest(BaseModel):
    message: str

class DecryptRequest(BaseModel):
    ciphertext: str

@app.post("/encrypt")
def encrypt_message(request: EncryptRequest):
    public_key_path = KEYS_DIR / "public_key.json"
    if not public_key_path.exists():
        raise HTTPException(status_code=400, detail="Public key not found.")

    with open(public_key_path, "r") as f:
        public_key = json.load(f)

    encrypted_data = encrypt(request.message, public_key)

    # Convert integer list to ASCII string
    encrypted_text = int_list_to_ascii_string(encrypted_data)

    return {"ciphertext": encrypted_text}


@app.post("/decrypt")
def decrypt_message(request: DecryptRequest):
    private_key_path = KEYS_DIR / "private_key.json"

    if not private_key_path.exists():
        raise HTTPException(status_code=400, detail="Private key not found.")

    with open(private_key_path, "r") as f:
        private_key = json.load(f)

    # Convert ASCII string back to integer list
    encrypted_list = ascii_string_to_int_list(request.ciphertext)

    decrypted_text = decrypt(encrypted_list, private_key)

    return {"message": decrypted_text}

class SaveKeysRequest(BaseModel):
    publicKey: str
    privateKey: str

@app.post("/save-keys")
def save_keys(request: SaveKeysRequest):
    """Save public and private keys as strings."""
    public_key_path = KEYS_DIR / "public_key.json"
    private_key_path = KEYS_DIR / "private_key.json"

    with open(public_key_path, "w") as f:
        f.write(request.publicKey)

    with open(private_key_path, "w") as f:
        f.write(request.privateKey)

    return {"message": "Keys saved successfully."}


class SaveEncryptedRequest(BaseModel):
    ciphertext: str

@app.post("/save-encrypted")
def save_encrypted(request: SaveEncryptedRequest):
    """Save encrypted text as a string."""
    encrypted_file = ENCRYPTED_DIR / "encrypted.txt"

    with open(encrypted_file, "w", encoding="utf-8") as f:  # Explicitly set encoding
        f.write(request.ciphertext)

    return {"message": "Encrypted text saved successfully.", "file_path": str(encrypted_file)}


class SaveDecryptedRequest(BaseModel):
    decryptedText: str

@app.post("/save-decrypted")
def save_decrypted(request: SaveDecryptedRequest):
    """Save decrypted message as a string."""
    decrypted_file = DECRYPTED_DIR / "decrypted.txt"

    with open(decrypted_file, "w") as f:
        f.write(request.decryptedText)

    return {"message": "Decrypted text saved successfully.", "file_path": str(decrypted_file)}
