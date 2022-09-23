from etc.bitarray import BitArray
import etc.DES.sdes as sdes

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
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("10010010001000010101111101011111000000001100101110110010011000000000000001011100010111110100001111110000")
    got = sdes.encrypt(plaintext, key)
    testcase(expected, got)

def text_decrypt_test():
    ciphertext = BitArray.fromBitString("10010010001000010101111101011111000000001100101110110010011000000000000001011100010111110100001111110000")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromString("Hello, World!", "utf-8")
    got = sdes.decrypt(ciphertext, key)
    testcase(expected, got)

simple_test()
decrypt_test()
text_test()
text_decrypt_test()















