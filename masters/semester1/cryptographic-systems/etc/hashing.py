import hashlib
import random
import string
from typing import Tuple

def sha2_to_int(message: 'str'):
    return int(sha2(message.encode('utf-8')), 16)

def random_hex_string(length: 'int') -> 'str':
    alphabet = string.digits + "ABCDEF"
    return ''.join(random.choices(alphabet, k = length))

def sha2(message: 'bytes') -> 'str':
    return hashlib.sha256(message).digest().hex()

def sha2_short(message: 'bytes', count: 'int') -> 'Tuple[str, str]':
    digest = sha2(message)
    return digest, digest[len(digest) - count: len(digest)]

def sha3(message: 'bytes') -> 'str':
    return hashlib.sha3_256(message).digest().hex()

def sha3_short(message: 'bytes', count: 'int') -> 'Tuple[str, str]':
    digest = sha3(message)
    return digest, digest[len(digest) - count: len(digest)]

# def strong_collision(fn):
#     while True:
#         _test_left = random_string(8)
#         _test_right = random_string(8)
#         digest1, _test_left_digest = fn(_test_left.encode("utf-8"), 2)
#         digest2, _test_right_digest = fn(_test_right.encode("utf-8"), 2)
#         if _test_left_digest == _test_right_digest:
#             return _test_left, _test_right, digest1, digest2, _test_left_digest