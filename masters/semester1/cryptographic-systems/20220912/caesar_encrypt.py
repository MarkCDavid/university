from caesar import CaesarCipher
from sys import argv as program_arguments
from string import ascii_uppercase

if __name__ == '__main__':
    plaintext = "I CAME, I SAW, I CONQUERED."
    if len(program_arguments) > 1:
        plaintext = program_arguments[1]
    
    offset = 3
    if len(program_arguments) > 2:
        offset = int(program_arguments[2])

    alphabet = ascii_uppercase
    if len(program_arguments) > 3:
        alphabet = program_arguments[3]

    caesar = CaesarCipher(alphabet=alphabet, offset=offset)
    ciphertext = caesar.compute(plaintext)
    
    print(f"{plaintext} ==CAESAR {offset}==> {ciphertext}")