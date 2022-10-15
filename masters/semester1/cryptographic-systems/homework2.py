from collections import Counter
from typing import Callable, Tuple
from etc.aeslib import AES, _pad
from etc.bitarray2 import BitArray2
from etc.extendedeuclidian import extendedEuclidian
from etc.hashing import sha2, sha3, sha2_short, sha3_short, random_hex_string

A = "AurimasSakalys"
B = 20185388
C = "VILNIUSGEDIMINASTECHNIKALUNIVERSITY"

B1 = 2018
B2 = 5388

print("=== Task 1:")

t1_result = extendedEuclidian(B1, B2)
print(f"GCD({B1}, {B2}) is {t1_result.gcd}")

t2_result = extendedEuclidian(B, 661)
print(f"Multiplicative inverse (mod 661) of {B} is {t2_result.bezout[0] % 661}")

print()
print()
print("=== Task 2:")

a_bitarray_initial: BitArray2 = BitArray2.fromString(A, "utf-8")
b_bitarray_initial: BitArray2 = BitArray2.fromInteger(B, "big")


a_bitarray_modified: BitArray2 = BitArray2.fromBitArray(a_bitarray_initial)
a_bitarray_modified[76] ^= 1

b_bitarray_modified: BitArray2 = BitArray2.fromBitArray(b_bitarray_initial)
b_bitarray_modified[12] ^= 1

print("Padding is done using PKCS7.")
print()
print("      Initial A (as bits):", a_bitarray_initial)
print("       Padded A (as bits):", _pad(a_bitarray_initial, 128))
print("Modified A [76] (as bits):", a_bitarray_modified)
print()
print("      Initial B (as bits):", b_bitarray_initial)
print("       Padded B (as bits):", _pad(b_bitarray_initial, 128))
print("Modified B [12] (as bits):", b_bitarray_modified)

b_initial_aes = AES(b_bitarray_initial)
b_modified_aes = AES(b_bitarray_modified)

a_initial_b_initial_encrypted = b_initial_aes.encrypt(a_bitarray_initial)
a_initial_b_modified_encrypted = b_modified_aes.encrypt(a_bitarray_initial)
a_modified_b_initial_encrypted = b_initial_aes.encrypt(a_bitarray_modified)

print()
print("AES Encryption:")
print(" Initial A with key Initial B (as bits):", a_initial_b_initial_encrypted)
print("Initial A with key Modified B (as bits):", a_initial_b_modified_encrypted)
print("Modified A with key Initial B (as bits):", a_modified_b_initial_encrypted)

b_modified_changed_bits = Counter([x == y for x, y in zip(a_initial_b_initial_encrypted, a_initial_b_modified_encrypted)])[False]
a_modified_changed_bits = Counter([x == y for x, y in zip(a_initial_b_initial_encrypted, a_modified_b_initial_encrypted)])[False]

print()
print(f"After modifying B, there were {b_modified_changed_bits} changed bits, when compared to original")
print(f"After modifying A, there were {a_modified_changed_bits} changed bits, when compared to original")

print()
print()
print("=== Task 3:")

print("As I am using Python to complete the homework, I've expanded the task to find collisions as follows:")
print("For weak collision, find collision using last 32 bits (2 hexadecimal symbols);")
print("For strong collision, find collision using last 64 bits (4 hexadecimal symbols).")
print()
print("SHA2 (256) of A is:", sha2(A.encode("utf-8")))
print("SHA3 (256) of A is:", sha3(A.encode("utf-8")))


def weak_collision(function: 'Callable[[bytes, int], Tuple[str, str]]', plaintext: 'str'):
    plaintext = plaintext.encode("utf-8")
    digest, digest_short = function(plaintext, 2)
    while True:
        test_plaintext = random_hex_string(16)
        test_digest, test_digest_short = function(test_plaintext.encode("utf-8"), 2)
        if digest_short == test_digest_short:
            return test_plaintext, digest_short, digest, test_digest


def strong_collision(function: 'Callable[[bytes, int], Tuple[str, str]]'):
    left = random_hex_string(32)
    while True:
        right = random_hex_string(32)
        left_digest, left_digest_short = function(left.encode("utf-8"), 4)
        right_digest, right_digest_short = function(right.encode("utf-8"), 4)
   
        if left_digest_short == right_digest_short:
            return left, left_digest, right, right_digest, left_digest_short

def weak_collision_exploitation(hash: 'str', hash_function, plaintext: 'str'):
    print()
    print(f"Perfoming \"Weak Collision\" exploitation for \"{hash}\"")
    collision_text, short_digest, digest, collision_digest = weak_collision(hash_function, plaintext)
    print(f"Given a plaintext \"{A}\", found a collision \"{collision_text}\" with \"{hash}\" of \"{short_digest}\"")
    print(f"Hash of {A} - {digest}")
    print(f"Hash of {collision_text}       - {collision_digest}")

def strong_collision_exploitation(hash: 'str', hash_function):
    print()
    print(f"Perfoming \"Strong Collision\" exploitation for \"{hash}\"")
    left, left_digest, right, right_digest, digest_short = strong_collision(hash_function)
    print(f"Found a collision between \"{left}\" and  \"{right}\" with \"{hash}\" of \"{digest_short}\"")
    print(f"Hash of {left} - {left_digest}")
    print(f"Hash of {right} - {right_digest}")

weak_collision_exploitation("SHA2 (shortened)", sha2_short, A)
weak_collision_exploitation("SHA3 (shortened)", sha3_short, A)

strong_collision_exploitation("SHA2 (shortened)", sha2_short)
strong_collision_exploitation("SHA3 (shortened)", sha3_short)

print()
print()
print("=== Bonus Task")
print("S-AES implementation has been done.")