# Homework
# Encode your name using:
#   A0Z25
#   ASCII
# Convert your student card number to (high-endian):
#   Binary
#   Hexadecimal
#   Octal
#   Base 7
#   Base 64
#   Base 58

import string
base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

name = "AurimasSakalys"
student_card_number = 20114231

def encode_a0z25(value):
    return ' '.join(
            str(string.ascii_lowercase.index(c))
            for c 
            in value.lower())

def encode_ascii(value):
    return ' '.join(
            str(ord(c)) 
            for c 
            in value)

def convert_to(value, base, _map):
    assert len(_map) >= base
    result = []
    while value > 0:
      result.append(_map[value % base])
      value = value // base
    return ' '.join(reversed(result))

def convert_to_base2(value):
    return convert_to(value, 2, string.digits)

def convert_to_base8(value):
    return convert_to(value, 8, string.digits)

def convert_to_base7(value):
    return convert_to(value, 7, string.digits)

def convert_to_base16(value):
    return convert_to(value, 16, string.hexdigits)

def convert_to_base58(value):
    return convert_to(value, 58, base58_alphabet)

def convert_to_base64(value):
    return convert_to(value, 64, base64_alphabet)

def encode_to_base64(_bytes):
    result = '' 
    offset = 0

    def _get(_bytes, index):
        return _bytes[index] if index < len(_bytes) else 0
    
    def _b1(_bytes, offset):
        index = (_get(_bytes, offset + 0) & 0b11111100) >> 2
        return base64_alphabet[index]

    def _b2(_bytes, offset):
        top_bits = (_get(_bytes, offset + 0) & 0b00000011) << 4 
        bot_bits = (_get(_bytes, offset + 1) & 0b11110000) >> 4
        index = top_bits | bot_bits 
        return base64_alphabet[index]

    def _b3(_bytes, offset):
        if offset + 1 >= len(_bytes):
            return '='
        top_bits = (_get(_bytes, offset + 1) & 0b00001111) << 2
        bot_bits = (_get(_bytes, offset + 2) & 0b11000000) >> 6
        index = top_bits | bot_bits
        return base64_alphabet[index]

    def _b4(_bytes, offset):
        if offset + 2 >= len(_bytes):
            return '='
        index = (_get(_bytes, offset + 2) & 0b00111111) >> 0
        return base64_alphabet[index]

    while offset < len(_bytes):
        result += _b1(_bytes, offset)
        result += _b2(_bytes, offset)
        result += _b3(_bytes, offset)
        result += _b4(_bytes, offset)
        offset += 3

    return result

print(encode_a0z25(name))
print(encode_ascii(name))
print(encode_to_base64(name.encode("utf-8")))

print(convert_to_base2(student_card_number))
print(convert_to_base7(student_card_number))
print(convert_to_base8(student_card_number))
print(convert_to_base16(student_card_number))
print(convert_to_base58(student_card_number))
print(convert_to_base64(student_card_number))
