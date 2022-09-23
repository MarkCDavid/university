import string

_base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _to(value, base, _map):
    assert len(_map) >= base
    result = []
    while value > 0:
      result.append(_map[value % base])
      value = value // base
    return ' '.join(reversed(result))

def base2(value):
    return _to(value, 2, string.digits)

def base8(value):
    return _to(value, 8, string.digits)

def base7(value):
    return _to(value, 7, string.digits)

def base16(value):
    return _to(value, 16, string.hexdigits)

def base58(value):
    return _to(value, 58, _base58_alphabet)

def base64(value):
    return _to(value, 64, _base64_alphabet)