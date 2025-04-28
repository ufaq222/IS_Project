# securefile_core.py
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey

backend = default_backend()

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=backend
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_rsa_keys(private_key, public_key, priv_path, pub_path):
    if not priv_path.endswith(".pem"):
        priv_path += "_private.pem"
    if not pub_path.endswith(".pem"):
        pub_path += "_public.pem"

    with open(priv_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(pub_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_public_key(path):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read(), backend=backend)

def load_private_key(path):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=backend)

def encrypt_file_rsa(file_path, public_key):
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    with open(file_path, 'rb') as f:
        data = f.read()

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    output_path = file_path + ".rsa.enc"
    with open(output_path, 'wb') as f:
        f.write(len(encrypted_key).to_bytes(4, 'big'))
        f.write(encrypted_key)
        f.write(iv)
        f.write(encrypted_data)

    return output_path

def decrypt_file_rsa(file_path, private_key):
    with open(file_path, 'rb') as f:
        key_len = int.from_bytes(f.read(4), 'big')
        encrypted_key = f.read(key_len)
        iv = f.read(16)
        encrypted_data = f.read()

    try:
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except InvalidKey:
        raise ValueError("Invalid RSA key or file format")

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    output_path = file_path.replace(".rsa.enc", ".dec")
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

    return output_path
