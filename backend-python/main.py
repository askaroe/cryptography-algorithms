import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from rsa_utils import generate_keys, encrypt, decrypt
from pydantic import BaseModel

# Set up logging
log_file_path = "logs/app_operations.log"  # Specify the log file path
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Open the log file in append mode (default is 'a')
)
logger = logging.getLogger(__name__)

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
    logger.info("Generating keys...")
    public_key, private_key = generate_keys()
    logger.info("Keys generated successfully.")
    return {"public_key": json.dumps(public_key), "private_key": json.dumps(private_key)}


class EncryptRequest(BaseModel):
    message: str

class DecryptRequest(BaseModel):
    ciphertext: str

@app.post("/encrypt")
def encrypt_message(request: EncryptRequest):
    logger.info("Starting encryption process...")

    public_key_path = KEYS_DIR / "public_key.json"
    if not public_key_path.exists():
        logger.error("Public key not found.")
        raise HTTPException(status_code=400, detail="Public key not found.")

    with open(public_key_path, "r") as f:
        public_key = json.load(f)

    encrypted_data = encrypt(request.message, public_key)

    # Convert integer list to ASCII string
    encrypted_text = int_list_to_ascii_string(encrypted_data)

    logger.info("Encryption successful.")
    return {"ciphertext": encrypted_text}


@app.post("/decrypt")
def decrypt_message(request: DecryptRequest):
    logger.info("Starting decryption process...")

    private_key_path = KEYS_DIR / "private_key.json"

    if not private_key_path.exists():
        logger.error("Private key not found.")
        raise HTTPException(status_code=400, detail="Private key not found.")

    with open(private_key_path, "r") as f:
        private_key = json.load(f)

    # Convert ASCII string back to integer list
    encrypted_list = ascii_string_to_int_list(request.ciphertext)

    decrypted_text = decrypt(encrypted_list, private_key)

    logger.info("Decryption successful.")
    return {"message": decrypted_text}


class SaveKeysRequest(BaseModel):
    publicKey: str
    privateKey: str

@app.post("/save-keys")
def save_keys(request: SaveKeysRequest):
    logger.info("Saving keys...")

    public_key_path = KEYS_DIR / "public_key.json"
    private_key_path = KEYS_DIR / "private_key.json"

    with open(public_key_path, "w") as f:
        f.write(request.publicKey)

    with open(private_key_path, "w") as f:
        f.write(request.privateKey)

    logger.info("Keys saved successfully.")
    return {"message": "Keys saved successfully."}


class SaveEncryptedRequest(BaseModel):
    ciphertext: str

@app.post("/save-encrypted")
def save_encrypted(request: SaveEncryptedRequest):
    logger.info("Saving encrypted text...")

    encrypted_file = ENCRYPTED_DIR / "encrypted.txt"

    with open(encrypted_file, "w", encoding="utf-8") as f:  # Explicitly set encoding
        f.write(request.ciphertext)

    logger.info(f"Encrypted text saved to {encrypted_file}.")
    return {"message": "Encrypted text saved successfully.", "file_path": str(encrypted_file)}


class SaveDecryptedRequest(BaseModel):
    decryptedText: str

@app.post("/save-decrypted")
def save_decrypted(request: SaveDecryptedRequest):
    logger.info("Saving decrypted text...")

    decrypted_file = DECRYPTED_DIR / "decrypted.txt"

    with open(decrypted_file, "w") as f:
        f.write(request.decryptedText)

    logger.info(f"Decrypted text saved to {decrypted_file}.")
    return {"message": "Decrypted text saved successfully.", "file_path": str(decrypted_file)}
