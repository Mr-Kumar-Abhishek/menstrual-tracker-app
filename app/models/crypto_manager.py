import os
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class CryptoManager:
    def __init__(self, key_path="secret.key"):
        self.key_path = self._resolve_path(key_path)
        self.cipher = self._initialize_cipher()

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

    def _initialize_cipher(self):
        try:
            if not os.path.exists(self.key_path):
                key = Fernet.generate_key()
                with open(self.key_path, "wb") as key_file:
                    key_file.write(key)
                logger.info(f"Generated new encryption key at {self.key_path}")
            else:
                with open(self.key_path, "rb") as key_file:
                    key = key_file.read()
            return Fernet(key)
        except Exception as e:
            logger.error(f"Failed to initialize crypto cipher: {e}")
            # If for some reason we cannot write the key file (e.g. read only fallback),
            # we should fallback to a volatile key so the app doesn't crash.
            return Fernet(Fernet.generate_key())

    def encrypt(self, data: str) -> str:
        if data is None:
            return None
        try:
            return self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data

    def decrypt(self, data: str) -> str:
        if data is None:
            return None
        try:
            return self.cipher.decrypt(data.encode('utf-8')).decode('utf-8')
        except Exception as e:
            # If decryption fails, it might be legacy unencrypted data or a bad key.
            # We return the raw data gracefully.
            return data
