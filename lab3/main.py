from rabin import Rabin


if __name__ == '__main__':
    input_filename = input('Input file: ')
    output_filename = input('Output file: ')
    mode = input('Mode? (e/d) ')

    rabin = Rabin(512)
    rabin.generate_keys()

    if mode == 'e':
        rabin.encrypt_file(input_filename, output_filename)
    elif mode == 'd':
        rabin.decrypt_file(input_filename, output_filename)
    else:
        raise Exception('Incorrect mode!')
    