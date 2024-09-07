import os
from gost28147_89 import GOST28147_89


def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()

def write_file(file_path: str, data: bytes) -> None:
    with open(file_path, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    key = os.urandom(32)
    iv = os.urandom(8)

    gost = GOST28147_89(key, iv)

    input_text = read_file('input.txt')

    encrypted_text = gost.encrypt(input_text)
    write_file('encrypted.txt', encrypted_text)

    decrypted_text = gost.decrypt(encrypted_text)
    write_file('decrypted.txt', decrypted_text)
