# Original task was to decrypt LEZMVIJKPJKLUVEKJ
from pydoc import plain
from caesar import CaesarCipher
from sys import argv as program_arguments
from string import ascii_uppercase

if __name__ == '__main__':
    ciphertext = "LEZMVIJKPJKLUVEKJ"
    if len(program_arguments) > 1:
        ciphertext = program_arguments[1]
    
    alphabet = ascii_uppercase
    if len(program_arguments) > 2:
        alphabet = program_arguments[2]

    for offset in range(len(alphabet)):
        caesar = CaesarCipher(alphabet=alphabet, offset=offset)
        plaintext = caesar.compute(ciphertext)

        print(f"{ciphertext} ==CAESAR {offset}==> {plaintext}")