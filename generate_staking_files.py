import base64
import os, binascii
from passlib.hash import pbkdf2_sha256
import varint
import hashlib
import numpy as np
import hashlib
import base58
from blake3 import blake3
import varint
import ed25519
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(data: str):
    salt = binascii.unhexlify('646464646464646464646464')
    salt_encoded = base64.b64decode(salt)
    key = hashlib.pbkdf2_hmac('sha256', b'massa', salt_encoded, 10000, 32)
    nonce = binascii.unhexlify('656565656565656565656565')
    cipher = AESGCM(key)
    encrypted = cipher.encrypt(nonce, data.encode("utf-8"), None)
    result = bytearray()
    result.extend(varint.encode(0))
    result.extend(salt)
    result.extend(nonce)
    result.extend(encrypted)
    return result

class KeyPair:
    def __init__(self, secret_key=None, public_key=None):
            self.secret_key = secret_key
            self.public_key = public_key
    
    def random():
        signing_key, verifying_key = ed25519.create_keypair()
        return KeyPair(secret_key=signing_key, public_key=verifying_key)

    def from_secret_massa_encoded(private: str):
        # Strip identifier
        private = private[1:]
        # Decode base58
        private = base58.b58decode_check(private)
        # Decode varint
        version = varint.decode_bytes(private)
        # Get rest (for the moment versions are little)
        secret_key = private[1:]
        # decode privkey
        secret_key = ed25519.keys.SigningKey(secret_key)
        public_key = secret_key.get_verifying_key()
        return KeyPair(secret_key=secret_key, public_key=public_key)

    def get_public_massa_encoded(self):
        return 'P' + base58.b58encode_check(varint.encode(0) + self.public_key.to_bytes()).decode("utf-8")

    def get_secret_massa_encoded(self):
        return 'S' + base58.b58encode_check(varint.encode(0) + self.secret_key.to_seed()).decode("utf-8")

def deduce_address(pubkey):
    return 'AU' + base58.b58encode_check(varint.encode(0) + blake3(pubkey.to_bytes()).digest()).decode("utf-8")

if __name__ == "__main__":
    # Find all files that have privkey.key in their name in the config folder
    files = os.listdir("config")
    privkey_files = [f for f in files if "privkey.key" in f]
    for f in privkey_files:
        # print(f)
        # Read the file
        # Strip file names
        file_name = f.split("_privkey.key")
        with open(f"config/{f}", "r") as f:
            content = json.loads(f.read())
            # Get the secret key
            secret_key = content["secret_key"]
            keypair = KeyPair.from_secret_massa_encoded(secret_key)
            content_staking = { deduce_address(keypair.public_key): { "secret_key": keypair.get_secret_massa_encoded(), "public_key": keypair.get_public_massa_encoded() } }
            with open(f"config/{file_name[0]}_staking_wallet.dat", "wb") as json_file:
                json_file.write(encrypt(json.dumps(content_staking)))
