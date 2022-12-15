from typing import List
from Crypto.Hash import SHA3_512, SHAKE128, SHAKE256
from Crypto.Random import get_random_bytes
from itertools import permutations, chain
from bitarray2 import BitArray2
from bitarray import BitArray
from parameters import PARAMETERS
from utility import to_unsigned_byte
# class KyberParams:

#     def __init__(self):
#         self.k = 2 # number of polynomials per vector
#         self.n = 256 # KYBER_N, maximum degree of polynomials used
#         self.q = 3329 # KYBER_Q, modulus for numbers
#         self.inverse_q = 62209 # KYBER_Q_INV

#         self.seed_size = 32 # KYBER_SYM_BYTES

#         # controlls how big coefficients for small vectors can be
#         self.eta1 = 3 # KYBER_ETAK512, KYBER_ETAK768_1024
#         self.eta2 = 2 # KYBER_ETAK768_1024

#         # controls how much (u,v) get compressed
#         self.du = 10,
#         self.dv = 4, 
#         self.polynomial_coefficient_count = 384

#         # Controls
#         self._static_bytes = [68, 17, 101, 2, -4, -78, -21, 4, -72, 25, -39, 126, -58, -3, -94, 37, 126, -53, 37, 68, 77, -48, -74, -26, 86, -24, 36, -67, 16, -7, 123, -11]
#         self._static = False

# KYBER_PARAMS = KyberParams()
# KYBER_PARAMS._static = True

# def to_signed_byte(x):
#     y = x & 0xff
#     if y >= 2**7:
#         y -= 2**8
#     return y
    
# def to_unsigned_byte(x):
#     return x & 0xff

# def to_signed_short(x):
#     y = x & 0xffff
#     if y >= 2**15:
#         y -= 2**16
#     return y
    
# def to_unsigned_short(x):
#     return x & 0xffff

# def to_signed_int(x):
#     y = x & 0xfffffff
#     if y >= 2**31:
#         y -= 2**32
#     return y
    
# def to_unsigned_int(x):
#     return x & 0xffffffff

# def generate_polynomial():
#     return [0 for _ in range(0, KYBER_PARAMS.polynomial_coefficient_count)]

# def generate_vector_of_polynomials():
#     return [generate_polynomial() for _ in range(0, KYBER_PARAMS.k)]

# def generate_seed_vector():
#     return [0 for _ in range(0, KYBER_PARAMS.seed_size)]

# def random_bytes():
#     if KYBER_PARAMS._static:
#         return bytearray([value & 0xFF for value in KYBER_PARAMS._static_bytes])
#     return get_random_bytes(KYBER_PARAMS.seed_size)

# def polynomial_indexes():
#     for i in range(0, KYBER_PARAMS.k):
#         for j in range(0, KYBER_PARAMS.k):
#             yield [i, j]


# def generate_seeds():
#     seed = [to_signed_byte(x) for x in SHA3_512.new(random_bytes()).digest()]
#     print(seed)
#     return (
#         seed[0 : KYBER_PARAMS.seed_size], 
#         seed[KYBER_PARAMS.seed_size : 2 * KYBER_PARAMS.seed_size]
#     )

# def generate_buffer(seed, index):
#     unsigned_seed = [to_unsigned_byte(x) for x in seed]
#     shake128 = SHAKE128.new()
#     shake128.update(bytearray(unsigned_seed))
#     shake128.update(bytearray(index[::-1]))
#     return [to_signed_byte(x) for x in shake128.read(672)]

# def generate_uniform(buffer, length):
#     r = [ 0 for x in range(0, KYBER_PARAMS.polynomial_coefficient_count) ]
#     i, j = 0, 0
#     while i < length and (j + 3) < len(buffer):
#         d1 = ((buffer[j + 0] & 0xFF) >> 0 | (buffer[j + 1] & 0xFF) << 8) & 0xFFF
#         d2 = ((buffer[j + 1] & 0xFF) >> 4 | (buffer[j + 2] & 0xFF) << 4) & 0xFFF
#         j += 3
#         if d1 < KYBER_PARAMS.q:
#             r[i] = d1
#             i += 1
#         if i < length and d2 < KYBER_PARAMS.q:
#             r[i] = d2
#             i += 1
#     return (r, i)



# def generate_A(seed):
#     A = [[0 for _ in range(0, KYBER_PARAMS.k)] for _ in range(0, KYBER_PARAMS.k)]
#     for polynomial_index in polynomial_indexes():
#         buffer = generate_buffer(seed, polynomial_index)
#         r, i = generate_uniform(buffer[0:504], KYBER_PARAMS.n)
#         while i < KYBER_PARAMS.n:
#             m, c = generate_uniform(buffer[504:672], KYBER_PARAMS.n - i)
#             for k in range(i, KYBER_PARAMS.n):
#                 r[k] = m[k - i]
#             i += c
#         A[polynomial_index[0]][polynomial_index[1]] = r
#     return A

# def get_noise_polynomial(seed, nonce):
#     size = KYBER_PARAMS.eta1 * (KYBER_PARAMS.n // 4)
#     hash = SHAKE256.new(bytearray([x & 0xFF for x in [*seed, nonce]])).read(size)
#     return [to_signed_byte(x) for x in hash]

# def montgomery_reduce(a):
#     u = to_signed_short(a * KYBER_PARAMS.inverse_q)
#     t = (u * KYBER_PARAMS.q)
#     if u >= 2**31:
#         u -= 2**32
#     t = a - t
#     t >>= 16
#     return t

# def barrett_reduce(a):
#     shift = 1 << 26
#     v = to_signed_short((shift + (KYBER_PARAMS.q // 2)) // KYBER_PARAMS.q)
#     t = to_signed_short((v * a) >> 26)
#     t = to_signed_short(t * KYBER_PARAMS.q)
#     res = to_signed_short(a - t)
#     return res

# NTT_ZETAS = [
#     2285, 2571, 2970, 1812, 1493, 1422, 287, 202, 3158, 622, 1577, 182, 962,
#     2127, 1855, 1468, 573, 2004, 264, 383, 2500, 1458, 1727, 3199, 2648, 1017,
#     732, 608, 1787, 411, 3124, 1758, 1223, 652, 2777, 1015, 2036, 1491, 3047,
#     1785, 516, 3321, 3009, 2663, 1711, 2167, 126, 1469, 2476, 3239, 3058, 830,
#     107, 1908, 3082, 2378, 2931, 961, 1821, 2604, 448, 2264, 677, 2054, 2226,
#     430, 555, 843, 2078, 871, 1550, 105, 422, 587, 177, 3094, 3038, 2869, 1574,
#     1653, 3083, 778, 1159, 3182, 2552, 1483, 2727, 1119, 1739, 644, 2457, 349,
#     418, 329, 3173, 3254, 817, 1097, 603, 610, 1322, 2044, 1864, 384, 2114, 3193,
#     1218, 1994, 2455, 220, 2142, 1670, 2144, 1799, 2051, 794, 1819, 2475, 2459,
#     478, 3221, 3021, 996, 991, 958, 1869, 1522, 1628 ]

# def ntt(r):
#     j = 0
#     k = 1
#     l = 128
#     while l >= 2:
#         start = 0
#         while start < 256:
#             zeta = NTT_ZETAS[k]
#             k = k + 1
#             j = start
#             while j < start + l:
#                 t = montgomery_reduce(zeta * r[j + l])
#                 r[j + l] = to_signed_short(r[j] - t)
#                 r[j] = to_signed_short(r[j] + t)
#                 j += 1
#             start = j + l
#         l >>= 1
#     return r


# secret_key_vector_of_polynomials = generate_vector_of_polynomials()
# public_key_vector_of_polynomials = generate_vector_of_polynomials()
# error_vector_of_polynomials = generate_vector_of_polynomials()

# public_seed, noise_seed = generate_seeds()
# A = generate_A(public_seed)

# nonce = 0
# for i in range(0, KYBER_PARAMS.k):
#     secret_key_vector_of_polynomials[i] = get_noise_polynomial(noise_seed, nonce)
#     nonce = to_signed_byte(nonce + 1)

# for i in range(0, KYBER_PARAMS.k):
#     error_vector_of_polynomials[i] = get_noise_polynomial(noise_seed, nonce)
#     nonce = to_signed_byte(nonce + 1)

# print(secret_key_vector_of_polynomials)
# print(error_vector_of_polynomials)
# # secret_key_vector_of_polynomials = [ntt(x) for x in secret_key_vector_of_polynomials]
# # secret_key_vector_of_polynomials = [[barrett_reduce(y) for y in x] for x in secret_key_vector_of_polynomials]

# # error_vector_of_polynomials = [ntt(x) for x in error_vector_of_polynomials]

# # for i in range(0, KYBER_PARAMS.k):
# #     temp = polyvec_pointwise_acc_mont(a[i], skpv, params_k)
# #     pkpv[i] = poly_to_mont(temp)

KYBER_POLY_BYTES = 384
KYBER_N = 256
KYBER_ETAK512 = 3
KYBER_ETAK768_1024 = 2
KYBER_Q_INV = 62209
KYBER_Q = 3329
KYBER_SYM_BYTES = 32
KYBER_POlYVEC_BYTES_512 = 2 * KYBER_POLY_BYTES
KYBER_POlYVEC_BYTES_768 = 3 * KYBER_POLY_BYTES
KYBER_POlYVEC_BYTES_1024 = 4 * KYBER_POLY_BYTES
KYBER_POLY_COMPRESSED_BYTES_512 = 128
KYBER_POLY_COMPRESSED_BYTES_768 = 128
KYBER_POLY_COMPRESSED_BYTES_1024 = 160
KYBER_POLYVEC_COMPRESSED_BYTES_K512 = 2 * 320
KYBER_POLYVEC_COMPRESSED_BYTES_K768 = 3 * 320
KYBER_POLYVEC_COMPRESSED_BYTES_K1024 = 4 * 352
KYBER_INDCPA_PUBLICKEYBYTES_K512 = KYBER_POlYVEC_BYTES_512 + KYBER_SYM_BYTES
KYBER_INDCPA_PUBLICKEYBYTES_K768 = KYBER_POlYVEC_BYTES_768 + KYBER_SYM_BYTES
KYBER_INDCPA_PUBLICKEYBYTES_K1024 = KYBER_POlYVEC_BYTES_1024 + KYBER_SYM_BYTES

# KYBER_512SK_BYTES is a constant representing the byte length of private keys in Kyber-512
KYBER_512SK_BYTES = KYBER_POlYVEC_BYTES_512 + ((KYBER_POlYVEC_BYTES_512 + KYBER_SYM_BYTES) + 2 * KYBER_SYM_BYTES)
KYBER_768SK_BYTES = KYBER_POlYVEC_BYTES_768 + ((KYBER_POlYVEC_BYTES_768 + KYBER_SYM_BYTES) + 2 * KYBER_SYM_BYTES)
KYBER_1024SK_BYTES = KYBER_POlYVEC_BYTES_1024 + ((KYBER_POlYVEC_BYTES_1024 + KYBER_SYM_BYTES) + 2 * KYBER_SYM_BYTES)

KYBER_INDCPA_SECRETKEY_BYTES_K512 = 2 * KYBER_POLY_BYTES
KYBER_INDCPA_SECRETKEY_BYTES_K768 = 3 * KYBER_POLY_BYTES
KYBER_INDCPA_SECRETKEY_BYTES_K1024 = 4 * KYBER_POLY_BYTES


KYBER_SS_BYTES = 32


def cast_to_byte(x):
    y = x & 0xff
    if y >= 2**7:
        y -= 2**8
    return y


def generate_prf_byte_array(l, key, nonce):
    """
    pseudo-random function to derive a deterministic array of random bytes
    from the supplied secret key and a nonce
    :param l: int (size of random byte array)
    :param key: byte array
    :param nonce: byte
    :return: random byte array (hash)
    """
    hash = [ 0 for x in range(l)]
    xof = SHAKE256.new()
    new_key = [ 0 for x in range(0, len(key) + 1)]
    for i in range(0, len(key)):
        new_key[i] = key[i]
    new_key[len(key)] = nonce
    new_key = [ x & 0xff for x in new_key]
    xof.update(bytearray(new_key))
    hash = xof.read(l)
    hash = [ cast_to_byte(x) & 0xFF for x in hash ]
    return hash







def convert_byte_to_32_bit_unsigned_int(x):
    r = x[0] & 0xff # to mask negative values
    r |= (x[1] & 0xff) << 8
    r |= (x[2] & 0xff) << 16
    r |= (x[3] & 0xff) << 24
    return r

def convert_byte_to_24_bit_unsigned_int(x):
    r = x[0] & 0xff
    r |= (x[1] & 0xff) << 8
    r |= (x[2] & 0xff) << 16
    return r


def cbd(buf, paramsK):
    r = [ 0 for x in range(0, KYBER_POLY_BYTES)]
    if(paramsK == 2):
        for i in range(0, KYBER_N // 4):
            t = convert_byte_to_24_bit_unsigned_int(buf[3 * i:])
            d = t & 0x00249249
            d = d + ((t >> 1) & 0x00249249)
            d = d + ((t >> 2) & 0x00249249)
            for j in range(0,4):
                a = ((d >> (6 * j + 0)) & 0x7)
                b = ((d >> (6 * j + KYBER_ETAK512)) & 0x7)
                r[4 * i + j] = (a - b)
    else:
        for i in range(0, KYBER_N // 8):
            t = convert_byte_to_32_bit_unsigned_int(buf[4 * i:])
            d = t & 0x55555555
            d = d + ((t >> 1) & 0x55555555)
            for j in range(0,8):
                a = ((d >> (4 * j + 0)) & 0x3)
                b = ((d >> (4 * j + KYBER_ETAK768_1024)) & 0x3)
                r[8 * i + j] = (a - b)
    return r


def get_noise_poly(seed, nonce, params_k):
    """
    generate a deterministic noise polynomial from a seed and nonce
    :param seed: byte array
    :param nonce: byte
    :param params_k: int
    :return: short array (poly)
    """
    l = None
    if(params_k == 2):
        l = KYBER_ETAK512 * KYBER_N // 4
    else:
        l = KYBER_ETAK768_1024 * KYBER_N // 4
    p = generate_prf_byte_array(l, seed, nonce)
    return cbd(p, params_k)


z = get_noise_poly(PARAMETERS._static_bytes, 0, 2)
zz = calulate_noise_polynomial(PARAMETERS._static_bytes, 0)

for x, y in zip(z, zz):
    if x != y:
        print("bad")
        exit()