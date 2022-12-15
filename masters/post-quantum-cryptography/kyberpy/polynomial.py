from kmath import montgomery_reduce
from polynomialbase import PolynomialBase
from parameters import PARAMETERS
from typing import Iterable
import numpy as np


class Polynomial(PolynomialBase):

    @staticmethod
    def empty() -> 'Polynomial':
        return Polynomial(np.int16(0) for _ in range(PARAMETERS.polynomial_coefficient_count))

    def add(self: 'Polynomial', other: 'Polynomial') -> 'Polynomial':
        return Polynomial(lhs + rhs for lhs, rhs in zip(self, other))

    def subtract(self: 'Polynomial', other: 'Polynomial') -> 'Polynomial':
        return Polynomial(lhs - rhs for lhs, rhs in zip(self, other))

    def reduce(self: 'Polynomial', modulo: 'np.int16') -> 'Polynomial':
        return Polynomial(coefficient % modulo for coefficient in self)

    def to_montgomery_domain(self: 'Polynomial') -> 'Polynomial':
        return Polynomial(montgomery_reduce(np.int64(x)) for x in self)

    def __init__(self: 'PolynomialBase', coefficients: 'Iterable[np.int16]') -> 'None':
        super().__init__(coefficients)

KYBER_Q_INV = 62209
KYBER_Q = 3329
def cast_to_short(x):
    y = x & 0xffff
    if y >= 2**15:
        y -= 2**16
    return y



for x in range(-7000, 7000, 343):
    print(x, montgomery_reduce(x), ((x + KYBER_Q // 2) % KYBER_Q))