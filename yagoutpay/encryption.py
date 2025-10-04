import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class EncryptionUtils:
    def __init__(self):
        self.iv = b"0123456789abcdef"  # From constants if moved

    def encrypt(self, text: str, key_b64: str) -> str:
        """Encrypt text using AES-256-CBC with PKCS7 padding"""
        try:
            key = base64.b64decode(key_b64)
            if len(key) != 32:
                raise ValueError(f"Invalid key length: {len(key)} bytes, expected 32")
            backend = default_backend()
            cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=backend)
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(text.encode()) + padder.finalize()
            ct = encryptor.update(padded_data) + encryptor.finalize()
            return base64.b64encode(ct).decode()
        except Exception as e:
            raise ValueError(f"Encryption error: {e}")

    def decrypt(self, crypt_b64: str, key_b64: str) -> str:
        """Decrypt text using AES-256-CBC with PKCS7 unpadding"""
        try:
            key = base64.b64decode(key_b64)
            if len(key) != 32:
                raise ValueError(f"Invalid key length: {len(key)} bytes, expected 32")
            crypt = base64.b64decode(crypt_b64)
            backend = default_backend()
            cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=backend)
            decryptor = cipher.decryptor()
            padtext = decryptor.update(crypt) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padtext) + unpadder.finalize()
            return data.decode()
        except Exception as e:
            raise ValueError(f"Decryption error: {e}")