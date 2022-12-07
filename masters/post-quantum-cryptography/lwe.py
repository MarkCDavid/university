import numpy as np
import random

def r(min, max, size):
    return np.random.randint(min, max + 1, size)

def decode(encoded, mod):
    step = mod / 4
    if encoded < step or encoded > 3 * step:
        return 0
    return 1

n = 4
p = 7
m = 3

s = r(0, p, n)

a = [
    r(0, p, n)
    for _
    in range(m)
]

e = r(-1, 1, m)

# s = [3, 4, 0, 6]
# a = [
#     [1, 6, 6, 2],
#     [6, 0, 5, 3],
#     [2, 5, 4, 1]
# ]
# e = [0, -1, 1]

print(s)
print(a)
print(e)

b = np.add((np.matmul(a, s) % p), e) % p

print(b)

S = random.sample(range(m), random.randint(1, m))
# S = [0, 2]

ea = [0] * n
eb = 0

for i in S:
    ea = (np.add(ea, a[i]) % p)
    eb = (eb + b[i] % p)

bit = random.randint(0, 1)
print()
print(bit)
if bit:
    eb = (eb + p // 2) % p

print(ea, eb)


dv = (eb - ((np.matmul(s, ea)) % p)) % p
v = decode(dv, p)

print(v)


