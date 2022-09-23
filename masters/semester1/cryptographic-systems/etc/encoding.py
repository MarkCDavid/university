import string

_base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def a0z25(value):
    return ' '.join(
            str(string.ascii_lowercase.index(c))
            for c 
            in value.lower())


def a1z26(value):
    return ' '.join(
            str(string.ascii_lowercase.index(c) + 1)
            for c 
            in value.lower())

def ascii(value):
    return ' '.join(
            str(ord(c)) 
            for c 
            in value)


def base64(_bytes):
    result = '' 
    offset = 0

    def _get(_bytes, index):
        return _bytes[index] if index < len(_bytes) else 0
    
    def _b1(_bytes, offset):
        index = (_get(_bytes, offset + 0) & 0b11111100) >> 2
        return _base64_alphabet[index]

    def _b2(_bytes, offset):
        top_bits = (_get(_bytes, offset + 0) & 0b00000011) << 4 
        bot_bits = (_get(_bytes, offset + 1) & 0b11110000) >> 4
        index = top_bits | bot_bits 
        return _base64_alphabet[index]

    def _b3(_bytes, offset):
        if offset + 1 >= len(_bytes):
            return '='
        top_bits = (_get(_bytes, offset + 1) & 0b00001111) << 2
        bot_bits = (_get(_bytes, offset + 2) & 0b11000000) >> 6
        index = top_bits | bot_bits
        return _base64_alphabet[index]

    def _b4(_bytes, offset):
        if offset + 2 >= len(_bytes):
            return '='
        index = (_get(_bytes, offset + 2) & 0b00111111) >> 0
        return _base64_alphabet[index]

    while offset < len(_bytes):
        result += _b1(_bytes, offset)
        result += _b2(_bytes, offset)
        result += _b3(_bytes, offset)
        result += _b4(_bytes, offset)
        offset += 3

    return result
