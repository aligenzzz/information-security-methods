import Crypto.Util.number
import Crypto.Random


class Rabin:
    bits = 0
    public_key = 0
    private_key = 0

    def __init__(self, bits: int) -> None:
        self.bits = bits

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
        converted = Crypto.Util.number.bytes_to_long(message.encode('utf-8'))
        bit_string = bin(converted)
        output = bit_string + bit_string[-6:]
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
            append = binary[-6:]
            binary = binary[:-6]

            if append == binary[-6:]:
                return i     
        return
    
    def convert_int_to_message(self, number: int) -> str:
        formatted_text = format(number, 'x')
        decrypted_text = bytes.fromhex(formatted_text).decode()
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
        with open(input_file, 'r') as file:
            input_text = file.read()

        encrypted_text = self.encrypt(input_text)

        with open(output_file, 'w') as file:
            file.write(encrypted_text)
            
    def decrypt_file(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'r') as file:
            input_text = file.read()

        decrypted_text = self.decrypt(int(input_text))
        
        with open(output_file, 'w') as file:
            file.write(decrypted_text)
