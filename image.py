# image.py (updated)
from Crypto.Cipher import AES, ChaCha20
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from PIL import Image
from cryptography.fernet import Fernet
import io
import os
import base64

# --- Helper Functions ---

def derive_key(password):
    """Derive a 32-byte AES/ChaCha20 key from the password."""
    return SHA256.new(password.encode()).digest()

def derive_fernet_key(password):
    """Use SHA256 to derive Fernet 32-byte key and base64 encode."""
    return base64.urlsafe_b64encode(SHA256.new(password.encode()).digest())

def hash_password(password):
    """Hash password using SHA256."""
    return SHA256.new(password.encode()).digest()

def save_password_hash(hash_value, hash_path):
    """Save the password hash to a file."""
    with open(hash_path, 'wb') as f:
        f.write(hash_value)

def load_password_hash(hash_path):
    """Load the password hash from a file."""
    with open(hash_path, 'rb') as f:
        return f.read()

def verify_password(password, hash_path):
    """Verify password by comparing its hash."""
    entered_hash = hash_password(password)
    saved_hash = load_password_hash(hash_path)
    return entered_hash == saved_hash

# --- AES Functions ---

def encrypt_image_aes(image_path, output_path, password):
    key = derive_key(password)
    password_hash = hash_password(password)

    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

    cipher = AES.new(key, AES.MODE_CBC)
    padded_data = pad(img_bytes, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    with open(output_path, 'wb') as f:
        f.write(cipher.iv)  # Save IV first
        f.write(encrypted_data)

    # Save the password hash
    save_password_hash(password_hash, output_path + '.hash')

    print(f"Encrypted image saved to {output_path}")
    print(f"Password hash saved to {output_path}.hash")

def decrypt_image_aes(encrypted_image_path, output_path, password):
    # Verify password
    if not verify_password(password, encrypted_image_path + '.hash'):
        print("❌ Incorrect password! Decryption aborted.")
        return False

    key = derive_key(password)

    with open(encrypted_image_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    img = Image.open(io.BytesIO(decrypted_data))
    img.save(output_path)

    print(f"Decrypted image saved to {output_path}")
    return True

# --- ChaCha20 Functions ---

def encrypt_image_chacha20(image_path, output_path, password):
    key = derive_key(password)
    password_hash = hash_password(password)

    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

    cipher = ChaCha20.new(key=key)
    encrypted_data = cipher.encrypt(img_bytes)

    with open(output_path, 'wb') as f:
        f.write(cipher.nonce)  # Save nonce
        f.write(encrypted_data)

    save_password_hash(password_hash, output_path + '.hash')

    print(f"ChaCha20 Encrypted image saved to {output_path}")
    print(f"Password hash saved to {output_path}.hash")

def decrypt_image_chacha20(encrypted_image_path, output_path, password):
    if not verify_password(password, encrypted_image_path + '.hash'):
        print("❌ Incorrect password! Decryption aborted.")
        return False

    key = derive_key(password)

    with open(encrypted_image_path, 'rb') as f:
        nonce = f.read(8)
        encrypted_data = f.read()

    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted_data = cipher.decrypt(encrypted_data)

    img = Image.open(io.BytesIO(decrypted_data))
    img.save(output_path)

    print(f"ChaCha20 Decrypted image saved to {output_path}")
    return True

# --- Fernet Functions ---

def encrypt_image_fernet(image_path, output_path, password):
    key = derive_fernet_key(password)
    password_hash = hash_password(password)

    fernet = Fernet(key)

    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

    encrypted_data = fernet.encrypt(img_bytes)

    with open(output_path, 'wb') as f:
        f.write(encrypted_data)

    save_password_hash(password_hash, output_path + '.hash')

    print(f"Fernet Encrypted image saved to {output_path}")
    print(f"Password hash saved to {output_path}.hash")

def decrypt_image_fernet(encrypted_image_path, output_path, password):
    if not verify_password(password, encrypted_image_path + '.hash'):
        print("❌ Incorrect password! Decryption aborted.")
        return False

    key = derive_fernet_key(password)
    fernet = Fernet(key)

    with open(encrypted_image_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    img = Image.open(io.BytesIO(decrypted_data))
    img.save(output_path)

    print(f"Fernet Decrypted image saved to {output_path}")
    return True