import string

from collections import Counter
import etc.conversion as conversion
import etc.encoding as encoding
import etc.caesar as caesar
import etc.vigenere as vigenere

from etc.bitarray import BitArray
import etc.DES.des as des

A = "AurimasSakalys"
B = 20185388
C = "VILNIUSGEDIMINASTECHNIKALUNIVERSITY"

print(f"=== Task 1:")
print(f"Encode \"{A}\" using A1Z26:", encoding.a1z26(A))
print(f"Encode \"{A}\" using ASCII:", encoding.ascii(A))
print(f"Convert \"{B}\" to Base2:", conversion.base2(B))
print(f"Convert \"{B}\" to Base8:", conversion.base8(B))
print(f"Convert \"{B}\" to Base16:", conversion.base16(B))
print(f"Convert \"{B}\" to Base58:", conversion.base58(B))
print(f"Convert \"{B}\" to Base64:", conversion.base64(B))
print()
print(f"As it is not 100% clear, if Base64 is meant as a conversion or encoding, Base64 encoding is included.")
print()
print(f"Encode \"{A}\" using Base64:", encoding.base64(A.encode("utf-8")))
print()
print()
print(f"=== Task 2:")
caesar_encrypt, caesar_decrypt = caesar.encrypt_decrypt_pair(alphabet=string.ascii_uppercase, offset=B%26)
vigenere_encrypt, vigenere_decrypt = vigenere.encrypt_decrypt_pair(alphabet=string.ascii_uppercase, key=A.upper())

caesar_ciphertext = caesar_encrypt.compute(A.upper())
caesar_plaintext = caesar_decrypt.compute(caesar_ciphertext)

vigenere_ciphertext = vigenere_encrypt.compute(C.upper())
vigenere_decrypt = vigenere_decrypt.compute(vigenere_ciphertext)
print(f"Encrypt \"{A}\" using Caesar Cipher with key {B} mod 26:", caesar_ciphertext)
print(f"Decrypt \"{caesar_ciphertext}\" using Caesar Cipher with key {B} mod 26:", caesar_plaintext)
print()
print(f"I am unsure why a key that contains symbols that are not in the alphabet are required to use.")
print(f"To encrypt \"{C}\" using Vigenere Cipher, will use \"{A}\" as the key.")
print()
print(f"Encrypt \"{C}\" using Vigenere Cipher with key \"{A}\":", vigenere_ciphertext)
print(f"Decrypt \"{vigenere_ciphertext}\" using Vigenere Cipher with key \"{A}\":", vigenere_decrypt)

print()
print()
print(f"=== Task 3:")

plaintext_A = BitArray.fromString(A, "utf-8")[:64]
key_B = BitArray.fromInteger(B, 64)

print(f"Converting \"{A}\" to 64-bit block plaintext:", plaintext_A.hex())
print(f"Converting \"{B}\" to 64-bit block key:", key_B.hex())

ciphertext_A = des.encrypt(plaintext_A, key_B)
print(f"Encrypting \"{A}\" using DES with key {key_B.hex()}:", ciphertext_A.hex())
print()

plaintext_A_switched = BitArray(plaintext_A.size, plaintext_A.bits)
plaintext_A_switched[24] = (1 + plaintext_A_switched[24]) % 2
print(f"Switching one bit (index 24) in plaintext:", plaintext_A_switched.hex())

ciphertext_A_switched = des.encrypt(plaintext_A_switched, key_B)
print(f"Encrypting \"{A}\" with one plaintext bit switched using DES with key {key_B.hex()}:", ciphertext_A_switched.hex())
changed_bits = Counter([x == y for (x, y) in zip(ciphertext_A, ciphertext_A_switched)])[False]
print(f"After a bit switch in the plaintext, {changed_bits} bits have changed.")
print()

key_B_switched = BitArray(key_B.size, key_B.bits)
key_B_switched[12] = (1 + key_B_switched[24]) % 2
print(f"Switching one bit (index 12) in key:", key_B_switched.hex())

ciphertext_A_switched = des.encrypt(plaintext_A, key_B_switched)
print(f"Encrypting \"{A}\" with one key bit switched using DES with key {key_B_switched.hex()}:", ciphertext_A_switched.hex())
changed_bits = Counter([x == y for (x, y) in zip(ciphertext_A, ciphertext_A_switched)])[False]
print(f"After a bit switch in the key, {changed_bits} bits have changed.")

print()
print()
print("Bonus task:")
print("This task was done with DES algorithm that I have coded myself.")

