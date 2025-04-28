# crypto_utils.py
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def generate_key(password: str) -> bytes:
    salt = b'\x00' * 16
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_text(password: str, message: str) -> bytes:
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(message.encode())


def decrypt_text(password: str, encrypted: bytes) -> str:
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(encrypted).decode()
