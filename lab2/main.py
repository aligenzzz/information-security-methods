import os
import string
import random
from stb3410131_2011 import STB3410131_2011


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()
    
def write_file(file_path: str, data: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

def get_init_vector():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(16, 16)))
    

if __name__ == '__main__':
    key = str(os.urandom(32))
    iv = get_init_vector()
    
    stb = STB3410131_2011(key, iv)
    
    input_text = read_file('input.txt')
    
    encrypted_text = stb.encrypt(input_text)
    write_file('encrypted.txt', encrypted_text)
    
    decrypted_text = stb.decrypt(encrypted_text)
    write_file('decrypted.txt', decrypted_text)
