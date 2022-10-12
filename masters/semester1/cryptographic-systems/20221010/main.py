# 1. AES (same as DES)
# 2. NameSurname - SHA2, SHA3 (last 1, find weak collision)
# 3. Any (x,y) - SHA2, SHA3 (last 2, find strong collision)

import hashlib
import random
import string

def random_string(length: 'int') -> 'str':
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k = length))

def sha2(message: 'bytes', count: 'int') -> 'str':
    digest = hashlib.sha256(message).digest().hex()
    return digest, digest[len(digest) - count: len(digest)]

def sha3(message: 'bytes', count: 'int') -> 'str':
    digest = hashlib.sha3_256(message).digest().hex()
    return digest, digest[len(digest) - count: len(digest)]

def weak_collision(fn, text: 'str'):
    _bytes = text.encode("utf-8")
    digest1, _bytes_digest = fn(_bytes, 1)

    while True:
        _test = random_string(8)
        digest2, _test_digest = fn(_test.encode("utf-8"), 1)
        if _test_digest == _bytes_digest:
            return text, _test, digest1, digest2, _bytes_digest

def strong_collision(fn):
    while True:
        _test_left = random_string(8)
        _test_right = random_string(8)
        digest1, _test_left_digest = fn(_test_left.encode("utf-8"), 2)
        digest2, _test_right_digest = fn(_test_right.encode("utf-8"), 2)
        if _test_left_digest == _test_right_digest:
            return _test_left, _test_right, digest1, digest2, _test_left_digest

name = "AurimasSakalys"
print(weak_collision(sha2, name))
print(weak_collision(sha3, name))

print(strong_collision(sha2))
print(strong_collision(sha3))
