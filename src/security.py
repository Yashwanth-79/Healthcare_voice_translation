import os
from cryptography.fernet import Fernet
import logging

class BasicSecurity:
    def __init__(self):
        self.encryption_key = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def encrypt_text(self, text):
        if isinstance(text, str):
            return self.cipher_suite.encrypt(text.encode()).decode()
        return text
    
    def decrypt_text(self, encrypted_text):
        if isinstance(encrypted_text, str):
            try:
                return self.cipher_suite.decrypt(encrypted_text.encode()).decode()
            except:
                return None
        return encrypted_text