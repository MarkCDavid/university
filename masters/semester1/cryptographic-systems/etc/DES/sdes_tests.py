from bitarray import BitArray
import sdes

# source: https://terenceli.github.io/assets/file/mimaxue/SDES.pdf

def testcase(expected: 'BitArray', got: 'BitArray'):
    print(f"Expected: {expected}")
    print(f"     Got: {got}")
    print(f"  Passed: {expected == got}")
    print()

def simple_test():
    plaintext = BitArray.fromBitString("00101000")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("10001010")
    got = sdes.encrypt(plaintext, key)
    testcase(expected, got)

def decrypt_test():
    ciphertext = BitArray.fromBitString("10001010")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("00101000")
    got = sdes.decrypt(ciphertext, key)
    testcase(expected, got)

def text_test():
    plaintext = BitArray.fromString("Hello, World!", "utf-8")
    print(plaintext)
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("01100100110010000000110100001101101111110100011001111111011101111011111100111100000011010010101011011001")
    got = sdes.encrypt(plaintext, key)
    testcase(expected, got)

def text_decrypt_test():
    ciphertext = BitArray.fromBitString("01100100110010000000110100001101101111110100011001111111011101111011111100111100000011010010101011011001")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromString("Hello, World!", "utf-8")
    got = sdes.decrypt(ciphertext, key)
    testcase(expected, got)

simple_test()
decrypt_test()
text_test()
text_decrypt_test()















