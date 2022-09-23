from bitarray import BitArray
import des

# source: https://terenceli.github.io/assets/file/mimaxue/SDES.pdf

def testcase(expected: 'BitArray', got: 'BitArray'):
    print(f"Expected: {expected}")
    print(f"     Got: {got}")
    print(f"  Passed: {expected == got}")
    print()

def text_test():
    plaintext = BitArray.fromString("hello, world!", "utf-8")
    key = BitArray.fromString("keychain", "utf-8")
    expected = BitArray.fromBitString("11010001111101110001100010111101011101101010011110011111110011011111111110000111000000100110110010010010010010101111000110110001")
    got = des.encrypt(plaintext, key)
    testcase(expected, got)

def text_decrypt_test():
    ciphertext = BitArray.fromBitString("11010001111101110001100010111101011101101010011110011111110011011111111110000111000000100110110010010010010010101111000110110001")
    key = BitArray.fromString("keychain", "utf-8")
    expected = BitArray.fromString("hello, world!", "utf-8")
    got = des.decrypt(ciphertext, key)
    testcase(expected, got)

text_test()
text_decrypt_test()















