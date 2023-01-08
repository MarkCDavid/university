from ntt import ntt, ntt_inverse, ntt_multiply_polynomial_vectors
from utility import Nonce, reduce
from parameters import PARAMETERS
from extendedeuclidian import moduloInverse
from operator import add

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

    secret_key_ntt = [reduce(ntt(k), PARAMETERS.q) for k in secret_key]
    error_ntt = [reduce(ntt(k), PARAMETERS.q) for k in error]

    public_key = [ntt_multiply_polynomial_vectors(a, secret_key_ntt) for a in A]
    public_key = [reduce(list(map(add, public, error)), PARAMETERS.q) for (public, error) in zip(public_key, error_ntt)]

    


key_generation()
