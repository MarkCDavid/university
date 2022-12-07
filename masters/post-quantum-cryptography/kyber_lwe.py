import numpy as np

def r(min, max, size):
    return np.random.randint(min, max + 1, size)

n = 7
p = 97

s = r(-1, 1, n)

a = [
    r(0, p, n)
    for _
    in range(n)
]   

bit = r(0, 1, 1)[0]
print("bit", bit)
e = r(-1, 1, n)

print("s", s)
print("a", a)
print("e", e)

b = np.add((np.matmul(a, s) % p), e) % p
print("b", b)

_r = r(-1, 1, n)
e_1 = r(-1, 1, n)

u = np.add((np.matmul(_r, a) % p), e_1) % p

print("_r", _r)
print("e_1", e_1)
print("u", u)

rb = np.matmul(_r, b) % p
print("rb", rb)

e_2 = r(-1, 1, 1)
v = (rb + e_2[0] + (bit * p//2)) % p

print("v", v)

us = np.matmul(u, s) % p

print("us", us)

pt = ((v - us) % p) / (p//2)

print("pt", pt)