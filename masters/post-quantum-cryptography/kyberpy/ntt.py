from parameters import PARAMETERS
from utility import chunk, reduce, recenter

TWO_INVERSE = 1665
ROOT_OF_UNITY = 17

ZETAS = {
    6: {
        0: 17, 1: 2761, 2: 583, 3: 2649, 4: 1637, 5: 723, 6: 2288, 7: 1100, 8: 1409, 9: 2662, 
        10: 3281, 11: 233, 12: 756, 13: 2156, 14: 3015, 15: 3050, 16: 1703, 17: 1651, 18: 2789, 19: 1789, 
        20: 1847, 21: 952, 22: 1461, 23: 2687, 24: 939, 25: 2308, 26: 2437, 27: 2388, 28: 733, 29: 2337, 
        30: 268, 31: 641, 32: 1584, 33: 2298, 34: 2037, 35: 3220, 36: 375, 37: 2549, 38: 2090, 39: 1645, 
        40: 1063, 41: 319, 42: 2773, 43: 757, 44: 2099, 45: 561, 46: 2466, 47: 2594, 48: 2804, 49: 1092, 
        50: 403, 51: 1026, 52: 1143, 53: 2150, 54: 2775, 55: 886, 56: 1722, 57: 1212, 58: 1874, 59: 1029, 
        60: 2110, 61: 2935, 62: 885, 63: 2154
    }, 
    5: {
        0: 289, 1: 331, 2: 3253, 3: 1756, 4: 1197, 5: 2304, 6: 2277, 7: 2055, 8: 650, 9: 1977, 
        10: 2513, 11: 632, 12: 2865, 13: 33, 14: 1320, 15: 1915, 16: 2319, 17: 1435, 18: 807, 19: 452, 
        20: 1438, 21: 2868, 22: 1534, 23: 2402, 24: 2647, 25: 2617, 26: 1481, 27: 648, 28: 2474, 29: 3110, 
        30: 1227, 31: 910
    }, 
    4: {
        0: 296, 1: 2447, 2: 1339, 3: 1476, 4: 3046, 5: 56, 6: 2240, 7: 1333, 8: 1426, 9: 2094, 
        10: 535, 11: 2882, 12: 2393, 13: 2879, 14: 1974, 15: 821
    }, 
    3: {
        0: 1062, 1: 1919, 2: 193, 3: 797, 4: 2786, 5: 3260, 6: 569, 7: 1746
    }, 
    2: {
        0: 2642, 1: 630, 2: 1897, 3: 848
    }, 
    1: {
        0: 2580, 1: 3289
    }, 
    0: {
        0: 1729
    }
}

ZETAS_INVERSE = {
    6: {
        0: 1175, 1: 2444, 2: 394, 3: 1219, 4: 2300, 5: 1455, 6: 2117, 7: 1607, 8: 2443, 9: 554, 
        10: 1179, 11: 2186, 12: 2303, 13: 2926, 14: 2237, 15: 525, 16: 735, 17: 863, 18: 2768, 19: 1230, 
        20: 2572, 21: 556, 22: 3010, 23: 2266, 24: 1684, 25: 1239, 26: 780, 27: 2954, 28: 109, 29: 1292, 
        30: 1031, 31: 1745, 32: 2688, 33: 3061, 34: 992, 35: 2596, 36: 941, 37: 892, 38: 1021, 39: 2390, 
        40: 642, 41: 1868, 42: 2377, 43: 1482, 44: 1540, 45: 540, 46: 1678, 47: 1626, 48: 279, 49: 314, 
        50: 1173, 51: 2573, 52: 3096, 53: 48, 54: 667, 55: 1920, 56: 2229, 57: 1041, 58: 2606, 59: 1692, 
        60: 680, 61: 2746, 62: 568, 63: 3312
    }, 
    5: {
        0: 2419, 1: 2102, 2: 219, 3: 855, 4: 2681, 5: 1848, 6: 712, 7: 682, 8: 927, 9: 1795, 
        10: 461, 11: 1891, 12: 2877, 13: 2522, 14: 1894, 15: 1010, 16: 1414, 17: 2009, 18: 3296, 19: 464, 
        20: 2697, 21: 816, 22: 1352, 23: 2679, 24: 1274, 25: 1052, 26: 1025, 27: 2132, 28: 1573, 29: 76, 
        30: 2998, 31: 3040
    }, 
    4: {
        0: 2508, 1: 1355, 2: 450, 3: 936, 4: 447, 5: 2794, 6: 1235, 7: 1903, 8: 1996, 9: 1089, 
        10: 3273, 11: 283, 12: 1853, 13: 1990, 14: 882, 15: 3033
    }, 
    3: {
        0: 1583, 1: 2760, 2: 69, 3: 543, 4: 2532, 5: 3136, 6: 1410, 7: 2267
    }, 
    2: {
        0: 2481, 1: 1432, 2: 2699, 3: 687
    }, 
    1: {
        0: 40, 1: 749
    }, 
    0: {
        0: 1600
    }
}

def ntt(polynomial):
    return ntt_recursive(polynomial[:256], 0, 0)

def ntt_recursive(polynomial, layer, index):
    if layer == 7:
        return polynomial

    size = len(polynomial)
    half_size = size // 2

    zeta = ZETAS[layer][index]

    bottom, top = polynomial[:half_size], polynomial[half_size:]
    top = reduce([zeta * t for t in top], PARAMETERS.q)

    left, right = (
        ntt_recursive([b + t for (b, t) in zip(bottom, top)], layer + 1, 2 * index + 0), 
        ntt_recursive([b - t for (b, t) in zip(bottom, top)], layer + 1, 2 * index + 1)
    )
    
    return reduce([*left, *right], PARAMETERS.q)

def ntt_inverse(polynomial):
    layer = 6
    size = 4
    half_size = 2

    for layer in range(6, -1, -1):
        chunks = list(chunk(polynomial, half_size))
        pairs = zip(chunks[0::2], chunks[1::2])
        for index, (left, right) in enumerate(pairs):
            zeta_inverse = ZETAS_INVERSE[layer][index]
            for offset in range(half_size):
                polynomial[size * index + offset            ] = (               TWO_INVERSE * (left[offset] + right[offset]))  % PARAMETERS.q
                polynomial[size * index + offset + half_size] = (zeta_inverse * TWO_INVERSE * (left[offset] - right[offset])) % PARAMETERS.q
        half_size = size
        size = size * 2
    
    return recenter(polynomial, PARAMETERS.q)

def ntt_multiply_polynomials(polynomialA, polynomialB, zeta):
    return reduce([
        polynomialA[1] * polynomialB[1] * zeta + polynomialA[0] * polynomialB[0], 
        polynomialA[0] * polynomialB[1] + polynomialA[1] * polynomialB[0]
    ], PARAMETERS.q)

def ntt_multiply_full_polynomials(polynomialA, polynomialB):
    result = []
    for i in range(PARAMETERS.n // 4):
        x = ntt_multiply_polynomials(polynomialA[4 * i + 0: 4 * i + 2], polynomialB[4 * i + 0: 4 * i + 2],  ZETAS[6][i])
        y = ntt_multiply_polynomials(polynomialA[4 * i + 2: 4 * i + 4], polynomialB[4 * i + 2: 4 * i + 4], -ZETAS[6][i])
        result.extend([*x, *y])
    return result

def ntt_multiply_polynomial_vectors(polynomialVectorA, polynomialVectorB):
    result = ntt_multiply_full_polynomials(polynomialVectorA[0], polynomialVectorB[0])
    for i in range(1, PARAMETERS.k):
        result_add = ntt_multiply_full_polynomials(polynomialVectorA[i], polynomialVectorB[i])
        result = [l + r for (l, r) in zip(result, result_add)]
    return reduce(result, PARAMETERS.q)