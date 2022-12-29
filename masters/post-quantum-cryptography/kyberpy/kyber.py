from ntt import ntt_recursive, ntt2, ntt, br7
from utility import Nonce, reduce
from parameters import PARAMETERS
from extendedeuclidian import moduloInverse

import A as _A
from symetricprimitives import G as _G
from symetricprimitives.PRF import PRF
from symetricprimitives.CBD import CBD


def key_generation():
    public_seed, noise_seed = _G.generate_seed()
    A = _A.generate(public_seed)

    nonce = Nonce(0)
    secret_key = [CBD(PARAMETERS.eta1, PRF(PARAMETERS.eta1, noise_seed, nonce.next())) for _ in range(PARAMETERS.k)]
    error = [CBD(PARAMETERS.eta1, PRF(PARAMETERS.eta1, noise_seed, nonce.next())) for _ in range(PARAMETERS.k)]

    nttt = ntt(secret_key[0])
    ntttr = ntt_recursive(secret_key[0], 0)

    print(ntttr)
    
    for index, pair in enumerate(zip(nttt, z)):
        if pair[0] == pair[1]:
            print("+", pair, index)
        if pair[0] != pair[1]:
            print("-", pair, index)

z = [1028, 1252, 299, 711, 3213, 231, 1392, 1871, 1674, 3008, 2209, 2522, 2680, 2677, 2357, 2699, 1282, 1951, 3023, 2985, 3196, 513, 883, 2321, 293, 706, 1143, 966, 2808, 342, 547, 3158, 2275, 1505, 579, 1571, 426, 1801, 1161, 2146, 2085, 1152, 610, 1245, 1204, 200, 1978, 2063, 2407, 1962, 368, 2435, 974, 1638, 2174, 2220, 1061, 53, 2667, 1465, 3159, 2859, 2757, 269, 2813, 498, 13, 1778, 1001, 452, 2628, 1389, 2838, 1739, 1072, 447, 1825, 380, 2826, 1266, 490, 2875, 151, 2722, 987, 944, 1233, 608, 74, 514, 260, 2592, 2833, 2232, 2255, 819, 3009, 2951, 1321, 2505, 250, 1533, 136, 1382, 2142, 1064, 709, 1234, 910, 2020, 2926, 1191, 488, 3009, 2711, 929, 769, 2323, 1392, 3030, 1743, 2365, 1770, 2407, 2765, 1065, 353, 2234, 2965, 1844, 51, 2876, 2292, 768, 282, 2163, 675, 765, 2706, 3157, 3213, 1091, 1611, 311, 85, 2427, 2712, 1469, 1126, 1468, 1857, 1939, 2235, 1661, 2154, 1097, 498, 1102, 636, 1245, 1699, 1102, 1985, 1158, 1917, 588, 2255, 3154, 195, 1042, 1050, 909, 91, 2633, 8, 193, 2814, 2076, 415, 1840, 266, 2449, 1486, 223, 21, 1112, 1903, 1673, 3292, 2344, 1960, 2887, 707, 2541, 133, 3028, 2977, 368, 274, 86, 3209, 620, 3024, 3311, 945, 423, 1567, 1354, 2150, 2765, 440, 2707, 2112, 1203, 3204, 968, 596, 360, 23, 1801, 650, 734, 2226, 3114, 464, 986, 709, 801, 1172, 2669, 134, 1350, 105, 2257, 2688, 571, 1361, 630, 2269, 936, 2924, 696, 252, 1876, 3135, 1654, 1086, 2602, 2617, 602, 2007, 2739, 2733, 2912, 1330, 2102]


print(z)
key_generation()


# error = [
#     generate_noise_polynomial(noise_seed, nonce.next())
#     for _
#     in range(PARAMETERS.k)
# ]

# print(ntt2(secret_key[0]))


# print(ntt(secret_key[0][0:256]))
# print(ntt_recursive(secret_key[0][0:256], 1))

# secret_key = [reduce(ntt(polynomial), PARAMETERS.q) for polynomial in secret_key]
# error = [ntt(polynomial) for polynomial in error]

# print(secret_key)
# print(error)
# # secret_key_vector_of_polynomials = [ntt(x) for x in secret_key_vector_of_polynomials]
# # secret_key_vector_of_polynomials = [[barrett_reduce(y) for y in x] for x in secret_key_vector_of_polynomials]

# # error_vector_of_polynomials = [ntt(x) for x in error_vector_of_polynomials]

# # for i in range(0, KYBER_PARAMS.k):
# #     temp = polyvec_pointwise_acc_mont(a[i], skpv, params_k)
# #     pkpv[i] = poly_to_mont(temp)
