import struct


class GOST28147_89:
    s_box = [
        [2, 6, 3, 14, 12, 15, 7, 5, 11, 13, 8, 9, 10, 0, 4, 1],
        [8, 12, 9, 6, 10, 7, 13, 1, 3, 11, 14, 15, 2, 4, 0, 5],
        [1, 5, 4, 13, 3, 8, 0, 14, 12, 6, 7, 2, 9, 15, 11, 10],
        [4, 0, 5, 10, 2, 11, 1, 9, 15, 3, 6, 7, 14, 12, 8, 13],
        [7, 9, 6, 11, 15, 10, 8, 12, 4, 14, 1, 0, 5, 3, 13, 2],
        [14, 8, 15, 2, 6, 3, 9, 13, 5, 7, 0, 1, 4, 10, 12, 11],
        [9, 13, 8, 5, 11, 4, 12, 2, 0, 10, 15, 14, 1, 7, 3, 6],
        [11, 15, 10, 8, 1, 14, 3, 6, 9, 0, 4, 5, 13, 2, 7, 12],
    ]
    
    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv

    # splits the key into eight 32-bit parts for 32 rounds of encryption
    def divide_key(self) -> list[int]:
        return [struct.unpack('<I', self.key[i*4:(i+1)*4])[0] for i in range(8)]

    # adds data padding
    def padding(self, data: bytes) -> bytes:
        exp_len = 8 - len(data) % 8
        return data + bytes([exp_len] * exp_len)

    # removes data padding
    def unpadding(self, data: bytearray) -> bytes:
        return data[: -data[-1]]

    def gost_round(self, N: int, key: int) -> int:
        temp = (N + key) % (1 << 32)
        result = 0

        for i in range(8):
            s_box_row = GOST28147_89.s_box[i][(temp >> (4 * i)) & 0xF]
            result |= s_box_row << (4 * i)

        return ((result << 11) | (result >> (32 - 11))) & 0xFFFFFFFF
 
    def encrypt_block(self, block: bytes) -> bytes:
        n1, n2 = struct.unpack('<II', block)
        key_parts = self.divide_key()

        for i in range(32):
            round_key = key_parts[i % 8]
            n1, n2 = n2 ^ self.gost_round(n1, round_key), n1

        return struct.pack('<II', n1, n2)

    def gamma_generator(self, counter: int) -> bytes:
        gamma_input = struct.pack('<Q', counter)
        gamma_block = bytes([self.iv[i] ^ gamma_input[i] for i in range(8)])
        return self.encrypt_block(gamma_block)

    def encrypt(self, text: bytes) -> bytes:
        text = self.padding(text)
        cipher_text = bytearray()

        counter = 0
        for i in range(0, len(text), 8):
            gamma = self.gamma_generator(counter)
            block = text[i:i+8]
            cipher_text.extend([block[j] ^ gamma[j] for j in range(len(block))])
            counter += 1

        return self.iv + cipher_text

    def decrypt(self, cipher_text: bytes) -> bytes:
        self.iv = cipher_text[:8]
        cipher_text = cipher_text[8:]

        text = bytearray()

        counter = 0
        for i in range(0, len(cipher_text), 8):
            gamma = self.gamma_generator(counter)
            block = cipher_text[i:i+8]
            text.extend([block[j] ^ gamma[j] for j in range(len(block))])
            counter += 1

        return self.unpadding(text)
    