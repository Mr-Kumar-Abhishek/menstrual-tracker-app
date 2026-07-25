import os
import logging
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

logger = logging.getLogger(__name__)

class CryptoManager:
    def __init__(self, key_path="secret.key"):
        self.key_path = self._resolve_path(key_path)
        self.key = self._initialize_key()

    def _resolve_path(self, path):
        if os.path.isabs(path):
            return path
        try:
            from kivy.app import App
            app = App.get_running_app()
            if app and app.user_data_dir:
                return os.path.join(app.user_data_dir, path)
        except Exception:
            pass
        return path

    def _initialize_key(self):
        try:
            if not os.path.exists(self.key_path):
                key = get_random_bytes(32) # AES-256
                with open(self.key_path, "wb") as key_file:
                    key_file.write(key)
                logger.info(f"Generated new encryption key at {self.key_path}")
                return key
            else:
                with open(self.key_path, "rb") as key_file:
                    key = key_file.read()
                    # A Fernet key might exist from previous version, which is urlsafe base64 of 32 bytes (44 chars).
                    # If the key is not exactly 32 bytes, we regenerate it so PyCryptodome doesn't crash.
                    if len(key) != 32:
                        logger.warning("Existing key length is invalid for raw AES-256. Generating a new key.")
                        new_key = get_random_bytes(32)
                        with open(self.key_path, "wb") as kf:
                            kf.write(new_key)
                        return new_key
                return key
        except Exception as e:
            logger.error(f"Failed to initialize crypto key: {e}")
            return get_random_bytes(32)

    def encrypt(self, data: str) -> str:
        if data is None:
            return None
        try:
            cipher = AES.new(self.key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
            encrypted_data = cipher.nonce + tag + ciphertext
            return "AES256GCM$" + base64.b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data

    def decrypt(self, data: str) -> str:
        if data is None:
            return None
        try:
            if not data.startswith("AES256GCM$"):
                # Check for legacy Fernet data which usually starts with 'gAAAA'
                if data.startswith("gAAAA"):
                    # We can't decrypt Fernet data easily without the cryptography lib or implementing Fernet in pycryptodome.
                    # For this prototype, we'll just return it as is or log a warning.
                    logger.warning("Found legacy Fernet ciphertext but we only support AES256GCM now.")
                    return data
                return data
                
            raw_b64 = data[len("AES256GCM$"):]
            encrypted_data = base64.b64decode(raw_b64)
            
            if len(encrypted_data) < 32:
                return data
                
            nonce = encrypted_data[:16]
            tag = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]
            
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        except Exception as e:
            return data
