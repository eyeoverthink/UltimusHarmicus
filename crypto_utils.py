from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json

def generate_keys():
    """Generates a new 2048-bit RSA key pair."""
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key

def sign(private_key_str: str, data: dict) -> str:
    """Signs a data dictionary using the private key."""
    key = RSA.import_key(private_key_str)
    h = SHA256.new(json.dumps(data, sort_keys=True).encode('utf-8'))
    signature = pkcs1_15.new(key).sign(h)
    return signature.hex()

def verify(public_key_str: str, data: dict, signature_hex: str) -> bool:
    """Verifies a signature for a data dictionary using the public key."""
    key = RSA.import_key(public_key_str)
    h = SHA256.new(json.dumps(data, sort_keys=True).encode('utf-8'))
    signature = bytes.fromhex(signature_hex)
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
