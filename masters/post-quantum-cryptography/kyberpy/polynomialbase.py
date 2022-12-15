
from typing import Iterable

import numpy as np


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