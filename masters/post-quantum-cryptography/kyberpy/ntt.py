from parameters import PARAMETERS
from utility import to_signed_short
import numpy as np
from extendedeuclidian import moduloInverse

# PARAMETERS.n - size
# PARAMETERS.q - prime number modulo


NTT_ZETAS = [
    2285, 2571, 2970, 1812, 1493, 1422, 287, 202, 3158, 622, 1577, 182, 962,
    2127, 1855, 1468, 573, 2004, 264, 383, 2500, 1458, 1727, 3199, 2648, 1017,
    732, 608, 1787, 411, 3124, 1758, 1223, 652, 2777, 1015, 2036, 1491, 3047,
    1785, 516, 3321, 3009, 2663, 1711, 2167, 126, 1469, 2476, 3239, 3058, 830,
    107, 1908, 3082, 2378, 2931, 961, 1821, 2604, 448, 2264, 677, 2054, 2226,
    430, 555, 843, 2078, 871, 1550, 105, 422, 587, 177, 3094, 3038, 2869, 1574,
    1653, 3083, 778, 1159, 3182, 2552, 1483, 2727, 1119, 1739, 644, 2457, 349,
    418, 329, 3173, 3254, 817, 1097, 603, 610, 1322, 2044, 1864, 384, 2114, 3193,
    1218, 1994, 2455, 220, 2142, 1670, 2144, 1799, 2051, 794, 1819, 2475, 2459,
    478, 3221, 3021, 996, 991, 958, 1869, 1522, 1628 ]

NTT_ZETAS_INV = [
    1701, 1807, 1460, 2371, 2338, 2333, 308, 108, 2851, 870, 854, 1510, 2535,
    1278, 1530, 1185, 1659, 1187, 3109, 874, 1335, 2111, 136, 1215, 2945, 1465,
    1285, 2007, 2719, 2726, 2232, 2512, 75, 156, 3000, 2911, 2980, 872, 2685,
    1590, 2210, 602, 1846, 777, 147, 2170, 2551, 246, 1676, 1755, 460, 291, 235,
    3152, 2742, 2907, 3224, 1779, 2458, 1251, 2486, 2774, 2899, 1103, 1275, 2652,
    1065, 2881, 725, 1508, 2368, 398, 951, 247, 1421, 3222, 2499, 271, 90, 853,
    1860, 3203, 1162, 1618, 666, 320, 8, 2813, 1544, 282, 1838, 1293, 2314, 552,
    2677, 2106, 1571, 205, 2918, 1542, 2721, 2597, 2312, 681, 130, 1602, 1871,
    829, 2946, 3065, 1325, 2756, 1861, 1474, 1202, 2367, 3147, 1752, 2707, 171,
    3127, 3042, 1907, 1836, 1517, 359, 758, 1441 ]

# def montgomery_reduce(a):
#     return a - (to_signed_short(a * PARAMETERS.inverse_q) * PARAMETERS.q) >> 16

# TODO: Refactor/simplify
def ntt(r):
    j = 0
    k = 1
    l = 128
    while l >= 2:
        start = 0
        while start < 256:
            zeta = NTT_ZETAS[k]
            k = k + 1
            j = start
            while j < start + l:
                t = montgomery_reduce(zeta * r[j + l])
                r[j + l] = to_signed_short(r[j] - t)
                r[j] = to_signed_short(r[j] + t)
                j += 1
            start = j + l
        l >>= 1
    return r

def montgomery_reduce(a):
    """
    :param a: big integer (i.e. long)
    :return: a reduced (16 bit signed short)
    """
    u = to_signed_short(a * 62209)
    t = (u * 3329)
    if u >= 2**31:
        u -= 2**32
    t = a - t
    t >>= 16
    return t


def polynomial_modulo_division(top, bot, modulo):
    remainder = top[::1]
    result = []
    inverse = moduloInverse(bot[0], modulo)
    for i in range(len(remainder) - len(bot) + 1):
        multiplier = (remainder[i] * inverse) % modulo
        result.append(multiplier)
        for j in range(len(bot)):
            remainder[i + j] = (remainder[i + j] - (bot[j] * multiplier % modulo)) % modulo
    return result, remainder[len(result):]



ZETA = 17


ZETAS = [((17**i) % PARAMETERS.q) for i in range(128)]
# ZETAS2 = [((17**i) * 2285) % PARAMETERS.q for i in range(128)]

# TREE = [
#   0, 64, 32, 96, 16, 80, 48, 112, 8, 72, 40, 104, 24, 88, 56, 120,
#   4, 68, 36, 100, 20, 84, 52, 116, 12, 76, 44, 108, 28, 92, 60, 124,
#   2, 66, 34, 98, 18, 82, 50, 114, 10, 74, 42, 106, 26, 90, 58, 122,
#   6, 70, 38, 102, 22, 86, 54, 118, 14, 78, 46, 110, 30, 94, 62, 126,
#   1, 65, 33, 97, 17, 81, 49, 113, 9, 73, 41, 105, 25, 89, 57, 121,
#   5, 69, 37, 101, 21, 85, 53, 117, 13, 77, 45, 109, 29, 93, 61, 125,
#   3, 67, 35, 99, 19, 83, 51, 115, 11, 75, 43, 107, 27, 91, 59, 123,
#   7, 71, 39, 103, 23, 87, 55, 119, 15, 79, 47, 111, 31, 95, 63, 127
# ];

# ZETAS3 = [ZETAS2[x] for x in TREE]

# print(ZETAS)
# print(ZETAS2)
# print(ZETAS3)

def ntt_recursive(P, k):
    n = len(P)
    if n == 1:
        return P
    Pe, Po = P[0::2], P[1::2]
    ye, yo = ntt_recursive(Pe, k + 1), ntt_recursive(Po, k + 1)
    y = [0] * n
    for j in range(n//2):
        y[j] = ye[j] + ZETAS[k]*yo[j] 
        y[j + n//2] = ye[j] - ZETAS[k]*yo[j]
    return y


def ntt2(signal):
    N = len(signal)
    zeta = 17
    zeta_powers = [((zeta ** x) % PARAMETERS.q) for x in range(N)]
    return [
        sum(
            signal[n] * zeta_powers[(n * f) % N]
            for n 
            in range(N)
        ) 
        for f 
        in range(N)
    ]