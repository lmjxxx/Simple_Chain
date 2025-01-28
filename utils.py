'''
Utility Functions

'''
import hashlib
from ecdsa import SigningKey, SECP256k1

def generate_private_key():
    return SigningKey.generate(curve=SECP256k1)

def generate_public_key(private_key):
    return private_key.verifying_key

def sign_message(private_key, message):
    return private_key.sign(message.encode())

def verify_signature(public_key, message, signature):
    return public_key.verify(signature, message.encode())

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

