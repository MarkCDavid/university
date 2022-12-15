import numpy as np
from typing import Iterable
from parameters import PARAMETERS
from kmath import montgomery_reduce

class PolynomialBase:

    def __init__(self: 'PolynomialBase', coefficients: 'Iterable[np.int16]') -> 'None':
        self.coefficients = list(coefficients)
    
    def __getitem__(self: 'PolynomialBase', index: 'int') -> 'np.int16':
        return self.coefficients[index]
    
    def __len__(self: 'PolynomialBase') -> 'int':
        return len(self.coefficients)

    def __str__(self: 'PolynomialBase') -> 'str':
        return f"[{', '.join(str(coefficient) for coefficient in self.coefficients)}]"

    def __repr__(self: 'PolynomialBase') -> 'str':
        return f"Polynomial({self})"

    def __iter__(self) -> 'PolynomialIterator':
        return PolynomialIterator(self)

class PolynomialIterator:

    def __init__(self: 'PolynomialIterator', polynomial: 'PolynomialBase') -> 'None':
        self.polynomial = polynomial
        self.index = 0
    
    def __next__(self: 'PolynomialIterator') -> 'np.int16':
        if self.index == len(self.polynomial):
            raise StopIteration
        
        coefficient = self.polynomial[self.index]
        self.index += 1
        return coefficient

    def __iter__(self) -> 'PolynomialIterator':
        return self


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
