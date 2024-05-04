from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class KeyPair(object):
    def __init__(self, private_key, public_key, passphrase):
        self.private_key = private_key
        self.public_key = public_key
        self.passphrase = passphrase

    def get_private_key(self):
        if self.private_key is None:
            raise ValueError("Private key is not available")

        return self.private_key

    def get_public_key(self):
        if self.public_key is None:
            raise ValueError("Public key is not available")

        return self.public_key

    def get_private_bytes(self):
        if self.passphrase is None:
            print(
                "WARNING: No passphrase provided. The private key WILL NOT be encrypted."
            )

        encryption = (
            serialization.BestAvailableEncryption(self.passphrase.encode("utf-8"))
            if self.passphrase
            else serialization.NoEncryption()
        )

        return self.get_private_key().private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption,
        )

    def get_public_bytes(self):
        return self.get_public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )


def generate_key_pair(passphrase: str):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

    return KeyPair(private_key, private_key.public_key(), passphrase)


def load_key_pair(private_key, public_key, passphrase):
    if passphrase is not None:
        passphrase = passphrase.encode("utf-8")

    if private_key is not None:
        private_key = serialization.load_pem_private_key(
            data=private_key, password=passphrase
        )

    if public_key is not None:
        public_key = serialization.load_pem_public_key(data=public_key)

    return KeyPair(private_key, public_key, passphrase)


def load_public_key_pair(public_key_bytes: bytes):
    return load_key_pair(None, public_key_bytes, None)


def load_private_key_pair(private_key_bytes: bytes, passphrase):
    return load_key_pair(private_key_bytes, None, passphrase)
