import numpy as np

def padd(x, y, m, pm):
    return pmod(np.polyadd(x, y) % m, pm)

def psub(x, y, m, pm):
    return pmod(np.polysub(x, y) % m, pm)

def pmul(x, y, m, pm):
    return pmod(np.polymul(x, y) % m, pm)

def pmod(x, mod):
    return np.polydiv(x, mod)[1]

def rpoly(min, max, size, mod):
    return pmod(np.random.randint(min, max + 1, size), mod)

def decode(encoded, mod):
    step = mod / 4
    if encoded < step or encoded > 3 * step:
        return 0
    return 1

m = 3
p = 71
n = 2 ** m
pl = [1, 0, 0, 0, 0, 0, 0, 0, 1]
l = 2

print(l)

a = rpoly(0, p, n, pl)
s = rpoly(-l, l, n, pl)
e = rpoly(-l, l, n, pl)

# a = [19, 10, 7, 18, 24, 24, 31, 0]
# s = [-1, 1, 2, -1, -1, 2, 1, 1]
# e = [1, -1, 1, 0, -1, -1, 0, 2]

b = padd(pmul(a, s, p, pl), e, p, pl)
print(b)

message = rpoly(0, 1, n, pl)
z = np.multiply(message, p // 2) % p

r = rpoly(-l, l, n, pl)
e1 = rpoly(-l, l, n, pl)
e2 = rpoly(-l, l, n, pl)

# r = [1, 0, 0, 3, 0, 0, -2, 1]
# e1 = [0, 1, 0, 0, 1, 0, -2, 0]
# e2 = [-1, 0, 2, -1, 0, -1, 0, 0]

u = padd(pmul(r, a, p, pl), e1, p, pl)
v = padd(padd(pmul(r, b, p, pl), e2, p, pl), z, p, pl)

print(u)
print(v)

d = pmod([decode(x, p) for x in psub(v, pmul(u, s, p, pl), p, pl)], pl)

print(message)
print(d)
