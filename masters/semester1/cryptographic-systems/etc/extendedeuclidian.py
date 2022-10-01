from collections import namedtuple
from typing import Tuple

ExtendedEuclidianResult = namedtuple('ExtendedEuclidianResult', ['gcd', 'bezout', 'quotients'])

def _next(previous: 'int', current: 'int', quotient: 'int') -> 'Tuple[int, int]':
    return (
        current, 
        previous - quotient * current
    )

def extendedEuclidian(a: 'int', b: 'int') -> 'ExtendedEuclidianResult':
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r > 0:
        quotient = old_r // r
        old_r, r = _next(old_r, r, quotient)
        old_s, s = _next(old_s, s, quotient)
        old_t, t = _next(old_t, t, quotient)
    
    return ExtendedEuclidianResult(old_r, (old_s, old_t), (s, t))