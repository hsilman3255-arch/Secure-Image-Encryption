from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def generate_keys(key_folder):

    public_key_path = os.path.join(key_folder, "public.pem")
    private_key_path = os.path.join(key_folder, "private.pem")

    if os.path.exists(public_key_path) and os.path.exists(private_key_path):
        return

    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_key_path, "wb") as f:
        f.write(private_key)

    with open(public_key_path, "wb") as f:
        f.write(public_key)


def encrypt_aes_key(aes_key, key_folder):

    public_key_path = os.path.join(key_folder, "public.pem")

    with open(public_key_path, "rb") as f:
        public_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(public_key)

    return cipher.encrypt(aes_key)


def decrypt_aes_key(encrypted_key, key_folder):

    private_key_path = os.path.join(key_folder, "private.pem")

    with open(private_key_path, "rb") as f:
        private_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(private_key)

    return cipher.decrypt(encrypted_key)