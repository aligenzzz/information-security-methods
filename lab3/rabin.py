import Crypto.Util.number
import Crypto.Random


class Rabin:
    bits = 0
    public_key = 0
    private_key = 0
    threshold = 0
    chunk_size = 0
    __encrypted_chunks = []

    def __init__(self, bits: int, threshold: int, chunk_size: int) -> None:
        self.bits = bits
        self.threshold = threshold
        self.chunk_size = chunk_size

    # p ≡ q ≡ 3 mod 4
    def generate_prime_number(self) -> int:
        while True:
            prime_number = Crypto.Util.number.getPrime(self.bits)
            if (prime_number % 4) == 3:
                break
        return prime_number
    
    def generate_keys(self) -> None:
        p = self.generate_prime_number()
        q = self.generate_prime_number()
        if p == q:
            return self.generate_keys()
        n = p * q
        self.public_key = n
        self.private_key = (p, q)

    def convert_message_to_int(self, message : str) -> int:
        converted = Crypto.Util.number.bytes_to_long(message.encode('utf-16'))
        bit_string = bin(converted)
        output = bit_string + bit_string[-self.threshold:]
        int_output = int(output, 2)
        return int_output

    # c = m² mod n
    def encrypt(self, message: str) -> str:
        message = self.convert_message_to_int(message)
        return str(pow(message, 2, self.public_key))
    
    # find greatest common divisor with euclidean algorithm
    def euclidean_algorithm(self, a: int, b: int) -> tuple[int]:
        if a == 0:
            return b, 0, 1
        else:
            gcd, y, x = self.euclidean_algorithm(b % a, a)
            return gcd, x - (b // a) * y, y
    
    def select_solution(self, solutions: list[int]) -> int:
        for i in solutions:
            binary = bin(i)
            append = binary[-self.threshold:]
            binary = binary[:-self.threshold]

            if append == binary[-self.threshold:]:
                return i     
        return
    
    def convert_int_to_message(self, number: int) -> str:
        formatted_text = format(number, 'x')        
        decrypted_text = bytes.fromhex(formatted_text).decode('utf-16', errors='ignore')
        return decrypted_text

    def decrypt(self, cipher: int) -> str:
        n = self.public_key
        p, q = self.private_key

        _, a, b = self.euclidean_algorithm(p, q)

        r = pow(cipher, (p + 1) // 4, p)
        s = pow(cipher, (q + 1) // 4, q)

        # chinese remainder theorem
        x = ((a * p * s + b * q * r) % n)
        y = ((a * p * s - b * q * r) % n)
        solutions = [x, n - x, y, n - y]

        plain_text = self.select_solution(solutions)

        string = bin(plain_text)
        string = string[:-6]
        plain_text = int(string, 2)

        decrypted_text = self.convert_int_to_message(plain_text)

        return decrypted_text

    def encrypt_file(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'rb') as file:
            input_bytes = file.read()
        input_text = input_bytes.decode('utf-16', errors='ignore') 
            
        chunks = [input_text[i:i + self.chunk_size] for i in range(0, len(input_text), self.chunk_size)]

        encrypted_chunks = []
        for chunk in chunks:
            encrypted_text = self.encrypt(chunk) 
            encrypted_chunks.append(encrypted_text)
        
        with open(output_file, 'w', encoding='utf-16') as file:
            for encrypted_chunk in encrypted_chunks:
                file.write(encrypted_chunk)
        
        self.__encrypted_chunks = encrypted_chunks
        
    def delete_empty_lines(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf-16') as file:
            lines = file.readlines()
            
        non_empty_lines = [line for line in lines if line.strip()]
        
        with open(filename, 'w', encoding='utf-16') as file:
            file.writelines(non_empty_lines)
            
    def decrypt_file(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'r', encoding='utf-16') as file:
            input_text = file.read()

        decrypted_chunks = []
        for chunk in self.__encrypted_chunks:
            decrypted_text = self.decrypt(int(chunk))
            decrypted_chunks.append(decrypted_text)
                    
        with open(output_file, 'w', encoding='utf-16') as file:
            for decrypted_chunk in decrypted_chunks:
                file.write(decrypted_chunk)
                
        self.delete_empty_lines(output_file)
