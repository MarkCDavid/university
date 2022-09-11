from math import gcd
from operator import mod
from congruential_generator import CongruentialGenerator
from cgencryptor import CGEncryptor

_A = 21
_B = 13
MODULO = 66
_SEED = 5

def modulo_division(x1, x2, modulo):
    x1 = x1 % modulo
    x2_inv = pow(x2, -1, modulo)
    return (x1 * x2_inv) % modulo

def _a(d1, d2, modulo):
    return modulo_division(d2, d1, modulo) % modulo

def _b(x0, x1, A, modulo):
    return (x1 - x0 * A) % modulo

def solve(x0, x1, x2, modulo):
    # If gcd between d1 and modulo is not 1 we are unable to perform modulo division
    # as modulo inverse of d1 does not exist. According to the paper below
    # https://www.staff.uni-mainz.de/pommeren/Cryptology/Bitstream/2_Analysis/LCGkm.pdf
    # we are able to perform the calculation by dividing the deltas and modulo by gcd.
    # This in turn, provides us with _A and _B such that 
    # A = _A + i * modulo, B = _B + j * modulo for i, j in {1, 2...}
    d1, d2 = x1 - x0, x2 - x1

    g = gcd(d1, modulo)
    if g != 1:
        d1, d2, modulo = d1 // g, d2 // g, modulo // g

    A = _a(d1, d2, modulo)
    B = _b(x0, x1, A, modulo)

    return A, B, modulo

cg = CongruentialGenerator(_A, _B, MODULO, _SEED)
cge = CGEncryptor(_A, _B, MODULO, _SEED)
plaintext = "Was certainty remaining engrossed applauded sir how discovery. Settled opinion how enjoyed greater joy adapted too shy. Now properly surprise expenses interest nor replying she she. Bore tall nay many many time yet less. Doubtful for answered one fat indulged margaret sir shutters together. Ladies so in wholly around whence in at. Warmth he up giving oppose if. Impossible is dissimilar entreaties oh on terminated. Earnest studied article country ten respect showing had. But required offering him elegance son improved informed."
ciphertext = cge.encrypt(plaintext, "utf-8")

plt_byte_count = (cge.modulo.bit_length() + 7) // 8

pt = [
    int.from_bytes(plaintext[plt_byte_count * 0: plt_byte_count * 1].encode("utf-8"), "little"), 
    int.from_bytes(plaintext[plt_byte_count * 1: plt_byte_count * 2].encode("utf-8"), "little"),
    int.from_bytes(plaintext[plt_byte_count * 2: plt_byte_count * 3].encode("utf-8"), "little")
]
bl = ((cge.modulo.bit_length() + 7) // 8) * 8
ct = []
for i in range(3):
    _ct = 0
    for j in range(bl):
        _ct |= (ciphertext.get(i * bl + j) << j)
    ct.append(_ct)

s1, s2, s3 = [(pt ^ ct) % MODULO for (pt, ct) in zip(pt, ct)]

A, B, modulo = solve(s1, s2, s3, MODULO)

for i in range(1):
    for j in range(1):
        A_ = A + i * modulo
        B_ = B + j * modulo
        cge2 = CGEncryptor(A_, B_, MODULO, s2)
        try:
            print(cge2.decrypt(ciphertext.shr(16), "utf-8"))
        except:
            pass