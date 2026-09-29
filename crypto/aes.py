from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def generate_key():
    return get_random_bytes(32)


def encrypt_file(input_file, output_file, key):

    cipher = AES.new(key, AES.MODE_CBC)

    with open(input_file, "rb") as f:
        data = f.read()

    encrypted_data = cipher.encrypt(
        pad(data, AES.block_size)
    )

    with open(output_file, "wb") as f:
        f.write(cipher.iv)
        f.write(encrypted_data)


def decrypt_file(input_file, output_file, key):

    with open(input_file, "rb") as f:

        iv = f.read(16)
        encrypted_data = f.read()

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    decrypted_data = unpad(
        cipher.decrypt(encrypted_data),
        AES.block_size
    )

    with open(output_file, "wb") as f:
        f.write(decrypted_data)