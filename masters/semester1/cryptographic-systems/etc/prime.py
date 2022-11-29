from random import sample 
from math import sqrt

def primes(to):
    sieve = [False] * (to + 1)
    primes = []
    for i in range(2, to + 1):
        if not sieve[i]:
            primes.append(i)
            for j in range(i * 2, to + 1, i):
                sieve[j] = True
    return primes

def is_prime(p):
    if p < 2: 
        return False
        
    for x in range(2, int(sqrt(p)) + 1):
        if p % x == 0:
            return False
    return True

def factorize(n):
    return [i for i in range(1, n + 1) if n % i == 0]

def random_prime(min, max):
    return sample(list(filter(lambda x: x > min, primes(max))), 1)[0]

def prime_totient(p, q):
    return (p - 1) * (q - 1)