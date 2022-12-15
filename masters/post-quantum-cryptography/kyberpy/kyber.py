
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

from ntt import ntt
from seed import generate_seed
from a import generate_A_matrix
from utility import Nonce, reduce
from parameters import PARAMETERS
from noise import generate_noise_polynomial

public_seed, noise_seed = generate_seed()
A = generate_A_matrix(public_seed)

nonce = Nonce(0)
secret_key = [
    generate_noise_polynomial(noise_seed, nonce.next())
    for _
    in range(PARAMETERS.k)
]

error = [
    generate_noise_polynomial(noise_seed, nonce.next())
    for _
    in range(PARAMETERS.k)
]

secret_key = [reduce(ntt(polynomial), PARAMETERS.q) for polynomial in secret_key]
error = [ntt(polynomial) for polynomial in error]

print(secret_key)
print(error)
# # secret_key_vector_of_polynomials = [ntt(x) for x in secret_key_vector_of_polynomials]
# # secret_key_vector_of_polynomials = [[barrett_reduce(y) for y in x] for x in secret_key_vector_of_polynomials]

# # error_vector_of_polynomials = [ntt(x) for x in error_vector_of_polynomials]

# # for i in range(0, KYBER_PARAMS.k):
# #     temp = polyvec_pointwise_acc_mont(a[i], skpv, params_k)
# #     pkpv[i] = poly_to_mont(temp)

