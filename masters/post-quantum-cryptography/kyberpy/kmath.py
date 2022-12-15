import numpy as np
from parameters import PARAMETERS
from random import getrandbits

def n_1_bits(n: 'int') -> 'int':
    y = getrandbits(n)
    return y | ~y

def montgomery_reduce(x: 'np.int64') -> 'np.int16':
    u = np.int16(x * PARAMETERS.inverse_q) * PARAMETERS.q
    return np.int16((x - u) >> 16)