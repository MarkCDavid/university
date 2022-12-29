from ntt import ntt_recursive, ntt2
from seed import generate_seed
from a import generate_A_matrix
from utility import Nonce, reduce
from parameters import PARAMETERS
from noise import generate_noise_polynomial
from extendedeuclidian import moduloInverse

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

print(ntt2(secret_key[0]))


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

