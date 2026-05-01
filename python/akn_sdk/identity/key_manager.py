# akn_sdk/identity/key_manager.py

from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder


class KeyManager:

    def __init__(self, private_key_base64: str = None):
        if private_key_base64:
            self.signing_key = SigningKey(
                private_key_base64.encode(),
                encoder=Base64Encoder
            )
        else:
            self.signing_key = SigningKey.generate()

        self.verify_key = self.signing_key.verify_key

    def get_private_key(self) -> str:
        return self.signing_key.encode(encoder=Base64Encoder).decode()

    def get_public_key(self) -> str:
        return self.verify_key.encode(encoder=Base64Encoder).decode()

    def sign(self, message_bytes: bytes) -> str:
        signed = self.signing_key.sign(message_bytes)
        return Base64Encoder.encode(signed.signature).decode()