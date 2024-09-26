from rabin import Rabin


if __name__ == '__main__':
    input_filename = 'input.txt'
    output_filename = 'encrypted.txt'
    decrypted_filename = 'decrypted.txt'

    rabin = Rabin(512, 6, 50)
    
    while True:
        try:
            rabin.generate_keys()

            rabin.encrypt_file(input_filename, output_filename)
            rabin.decrypt_file(output_filename, decrypted_filename)

            break
        except Exception as e:
            pass
        