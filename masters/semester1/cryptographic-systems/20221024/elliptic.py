from extendedeuclidian import extendedEuclidian 
from collections import namedtuple
  
Pair = namedtuple('Pair', ['x', 'y'])

A = 1
B = -3
P = 23

def get_λ(p: 'Pair', q: 'Pair') -> 'int':
    if p == q:
        top = 3 * (p.x ** 2) + A  
        bot = 2 * p.y 
    else:
        top = q.y - p.y
        bot = q.x - p.x
    inv_bot = extendedEuclidian(bot, P).bezout[0]
    return (top * inv_bot) % P

def get_R(p: 'Pair', q: 'Pair') -> 'Pair':
    λ = get_λ(p, q)
    x = (λ**2 - p.x - q.x) % P
    y = (λ * (p.x - x) - p.y) % P
    return Pair(x, y)

def elliptic(p: 'Pair', q: 'Pair') -> 'Pair':
    print("λ =", get_λ(p, q))
    print("R =", get_R(p, q))


p = Pair(3, 10)
q = Pair(9, 7)

elliptic(p, q)
elliptic(p, p)

p = Pair(11, 3)
q = Pair(0, 1)

elliptic(p, q)
